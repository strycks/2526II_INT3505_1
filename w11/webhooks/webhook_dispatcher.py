from threading import Thread
import requests


def dispatch(webhooks, event_type, data):
    for wh in webhooks:
        if wh["event"] != event_type:
            continue
        Thread(target=_send, args=(wh["url"], event_type, data), daemon=True).start()


def _send(url, event_type, data):
    import json
    from datetime import datetime
    payload = {"event": event_type, "timestamp": datetime.now().isoformat(), "data": data}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"[WEBHOOK] Sent {event_type} to {url} -> {resp.status_code}")
    except Exception as e:
        print(f"[WEBHOOK] Failed to send {event_type} to {url}: {e}")
