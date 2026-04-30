"""
Shared email tracking helper for all newsletters.
Logs sends to D1 and embeds tracking pixel in HTML.

Usage:
    from track_helper import embed_pixel, log_send

    # Before sending: embed pixel in HTML
    send_id = uuid.uuid4().hex
    html_with_pixel = embed_pixel(html, send_id)

    # After successful send: log to D1
    log_send(send_id, list_slug, email, subject)
"""
import os
import requests

WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev"


def embed_pixel(html, send_id):
    """Embed a 1x1 tracking pixel before </body>."""
    pixel_tag = f'<img src="{WORKER_URL}/track/open?sid={send_id}" width="1" height="1" alt="" style="display:none;border:0;" />'
    if '</body>' in html:
        return html.replace('</body>', f'{pixel_tag}</body>')
    return html + pixel_tag


def log_send(send_id, list_slug, email, subject):
    """Log a successful send to D1 via the newsletter worker."""
    api_secret = os.environ.get('API_SECRET') or os.environ.get('NEWSLETTER_API_SECRET', '')
    if not api_secret:
        return  # Silent fail — don't break sends if secret missing
    try:
        requests.post(
            f"{WORKER_URL}/track/send",
            json={"id": send_id, "list_slug": list_slug, "email": email, "subject": subject},
            headers={"Authorization": f"Bearer {api_secret}"},
            timeout=5,
        )
    except Exception:
        pass  # Never break email sending for tracking
