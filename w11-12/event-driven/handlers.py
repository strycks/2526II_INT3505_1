from datetime import datetime


audit_log = []


def audit_logger(event_type, data):
    entry = {"event": event_type, "data": data, "timestamp": datetime.now().isoformat()}
    audit_log.append(entry)
    print(f"[EVENT] {event_type}: {data.get('title', data.get('id', ''))}")


search_index = {}


def search_indexer(event_type, data):
    if event_type == "book.created":
        search_index[data["id"]] = data["title"].lower()
    elif event_type == "book.updated":
        if data["id"] in search_index:
            search_index[data["id"]] = data["title"].lower()
    elif event_type == "book.deleted":
        search_index.pop(data["id"], None)


def get_indexed_titles():
    ids = list(search_index.keys())
    return sorted(ids)
