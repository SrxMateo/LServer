"""Alertas Discord/Telegram via webhooks para LServer."""
import json
from lserver.state import set_setting, get_setting, remove_setting
from lserver.ui import log_success, log_info, log_error

def set_webhook(url):
    set_setting('webhook_url', url)
    if 'api.telegram.org' in url:
        log_success(f"Webhook de Telegram configurado.")
    else:
        log_success(f"Webhook de Discord configurado.")

def get_webhook():
    return get_setting('webhook_url')

def remove_webhook():
    remove_setting('webhook_url')
    log_success("Webhook eliminado.")

def send_alert(title, message, color=0xFF6600):
    """Envia una alerta al webhook configurado. Nunca crashea."""
    url = get_webhook()
    if not url:
        return
    
    try:
        import urllib.request
        
        if 'api.telegram.org' in url:
            # Formato Telegram Bot API
            text = f"*{title}*\n{message}"
            payload = json.dumps({
                "chat_id": url.split("/")[-1] if "/" in url else "",
                "text": text,
                "parse_mode": "Markdown"
            }).encode('utf-8')
            # Para Telegram, la URL debe ser completa (el usuario pasa la URL del bot + chat_id)
            # Formato esperado: https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>
            payload = json.dumps({
                "text": f"🔔 *{title}*\n{message}",
                "parse_mode": "Markdown"
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload,
                                        headers={'Content-Type': 'application/json',
                                                 'User-Agent': 'LServer-Alert'})
        else:
            # Formato Discord Webhook (Embed)
            payload = json.dumps({
                "embeds": [{
                    "title": f"🔔 {title}",
                    "description": message,
                    "color": color,
                    "footer": {"text": "LServer CLI - Lumax Studio"}
                }]
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload,
                                        headers={'Content-Type': 'application/json',
                                                 'User-Agent': 'LServer-Alert'})
        
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log_error(f"No se pudo enviar la alerta webhook: {e}")
