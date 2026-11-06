"""Privacy-conscious Hindi-first SUNDARAM study bot.

Looks up public educational/general-knowledge summaries on Wikipedia only.
Set TELEGRAM_BOT_TOKEN in the environment; never hard-code or commit the token.
"""

import html
import logging
import os
import re
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import json

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
USER_AGENT = "SundaramStudyBot/1.0 (educational Telegram bot)"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sundaram-bot")

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d ()-]{7,}\d)(?!\w)")
PRIVATE_LOOKUP_TERMS = re.compile(
    r"\b(phone number|mobile number|email address|home address|private address|"
    r"password|login|account access|personal details|private details|locate|"
    r"dox|leak|leaked data)\b",
    re.IGNORECASE,
)


def http_json(url, payload=None, timeout=25):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
        method="GET" if body is None else "POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def telegram(method, payload=None):
    result = http_json(f"{TELEGRAM_API}/{method}", payload)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error for {method}")
    return result["result"]


def send_text(chat_id, text):
    # Plain text avoids Markdown/HTML injection from user queries or source content.
    telegram("sendMessage", {"chat_id": chat_id, "text": text[:4000]})


def is_private_lookup(text):
    return bool(EMAIL_RE.search(text) or PHONE_RE.search(text) or PRIVATE_LOOKUP_TERMS.search(text))


def search_wikipedia(query):
    """Find one public encyclopedia summary (Hindi first, English fallback)."""
    for language in ("hi", "en"):
        api_url = f"https://{language}.wikipedia.org/w/api.php?" + urlencode(
            {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": 1,
                "utf8": 1,
            }
        )
        result = http_json(api_url)
        hits = result.get("query", {}).get("search", [])
        if not hits:
            continue
        page_id = hits[0]["pageid"]
        extract_url = f"https://{language}.wikipedia.org/w/api.php?" + urlencode(
            {
                "action": "query",
                "format": "json",
                "pageids": page_id,
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "exchars": 1000,
            }
        )
        pages = http_json(extract_url).get("query", {}).get("pages", {})
        page = pages.get(str(page_id), {})
        extract = re.sub(r"\s+", " ", page.get("extract", "")).strip()
        title = page.get("title", hits[0].get("title", "Wikipedia"))
        if extract:
            link = f"https://{language}.wikipedia.org/?curid={page_id}"
            return f"{title}\n\n{extract}\n\nस्रोत: {link}"
    return None


def handle_message(message):
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()
    if not chat_id or not text:
        return

    command = text.split(maxsplit=1)[0].split("@", 1)[0].lower()
    if command == "/start":
        send_text(
            chat_id,
            "नमस्ते! मैं SUNDARAM Study Bot हूँ। सामान्य ज्ञान या पढ़ाई के किसी विषय पर सवाल लिखें; मैं Wikipedia का सार्वजनिक सारांश और स्रोत खोजूँगा।\n\n"
            "मैं निजी फोन/ईमेल, पासवर्ड, निजी जानकारी या किसी खाते का access खोजने में मदद नहीं करता।\n"
            "कमांड: /help",
        )
        return
    if command == "/help":
        send_text(chat_id, "हिंदी या English में पढ़ाई/सामान्य ज्ञान का सवाल भेजें। उदाहरण: भारत का संविधान कब लागू हुआ? निजी जानकारी या account access न भेजें।")
        return
    if text.startswith("/"):
        send_text(chat_id, "यह कमांड उपलब्ध नहीं है। मदद के लिए /help भेजें।")
        return
    if is_private_lookup(text):
        send_text(chat_id, "मैं किसी व्यक्ति की निजी जानकारी, संपर्क विवरण, password या account access खोजने में मदद नहीं कर सकता। पढ़ाई या सामान्य ज्ञान का सवाल पूछें।")
        return
    if len(text) > 300:
        send_text(chat_id, "कृपया अपना शैक्षिक सवाल 300 अक्षरों से कम में भेजें।")
        return

    try:
        answer = search_wikipedia(text)
        send_text(chat_id, answer or "इस सवाल के लिए Wikipedia पर उपयुक्त सारांश नहीं मिला। कृपया विषय को थोड़ा स्पष्ट करके पूछें।")
    except Exception:
        log.exception("Question lookup failed")
        send_text(chat_id, "अभी जवाब खोजने में समस्या हुई। कृपया थोड़ी देर बाद फिर कोशिश करें।")


def main():
    if not TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in the environment; do not put it in source code.")
    # Long polling cannot run while a webhook is set.
    telegram("deleteWebhook", {"drop_pending_updates": False})
    offset = None
    log.info("Study bot polling started")
    while True:
        params = {"timeout": 50}
        if offset is not None:
            params["offset"] = offset
        try:
            updates = http_json(f"{TELEGRAM_API}/getUpdates?{urlencode(params)}", timeout=60)
            if not updates.get("ok"):
                raise RuntimeError("Telegram polling request failed")
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                try:
                    if "message" in update:
                        handle_message(update["message"])
                except Exception:
                    log.exception("Could not process update %s", update.get("update_id"))
        except KeyboardInterrupt:
            log.info("Study bot stopped")
            return
        except Exception:
            log.exception("Polling failed; retrying shortly")
            import time
            time.sleep(3)


if __name__ == "__main__":
    main()
