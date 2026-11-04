SUNDARAM.ORG — Updated website package
Your supplied photo is included and appears as the first large welcome/hero image immediately below the navigation bar.

Files:
- index.html
- assets/sundaram-founder-photo.png

FREE PUBLISHING WITH GITHUB PAGES:
1. Sign in to GitHub and create a PUBLIC repository named sundaram-org-site.
2. Upload index.html and the complete assets folder (do not upload index.html alone).
3. Repository Settings → Pages → Deploy from a branch → main → /(root) → Save.
4. Wait for GitHub to show the temporary *.github.io website URL.
5. In Settings → Pages → Custom domain, enter sundaram.org and Save.
6. In your domain registrar's DNS settings, add the GitHub Pages DNS records shown in GitHub's official instructions. For an apex domain, GitHub currently documents A records:
   @ → 185.199.108.153
   @ → 185.199.109.153
   @ → 185.199.110.153
   @ → 185.199.111.153
   Optional www CNAME should point to YOUR-GITHUB-USERNAME.github.io (replace with your real username).
7. Do not delete unrelated mail records (MX/TXT) or change nameservers unless you know why. Remove conflicting old web A/AAAA records only after checking the current DNS zone.
8. DNS changes can take up to 24 hours. When GitHub verifies the domain, enable Enforce HTTPS.

Important:
- Never share your domain registrar password, GitHub password, OTP, or recovery codes in chat.
- A live site cannot be confirmed until the repository is deployed and DNS is configured.
- The package is a static starter website. Actual uploaded lessons, PDFs, videos, student logins, admin panel, and message-delivering contact forms need additional implementation.
