import requests
import time

BASE = "http://127.0.0.1:5003"

# 1. Register a webhook pointing to our local test receiver
r = requests.post(f"{BASE}/webhooks", json={
    "url": f"{BASE}/webhook-test-receiver",
    "event": "book.created",
})
print(f"Registered webhook for book.created: {r.json()}")
assert r.status_code == 201

r = requests.post(f"{BASE}/webhooks", json={
    "url": f"{BASE}/webhook-test-receiver",
    "event": "book.updated",
})
print(f"Registered webhook for book.updated: {r.json()}")

r = requests.post(f"{BASE}/webhooks", json={
    "url": f"{BASE}/webhook-test-receiver",
    "event": "book.deleted",
})
print(f"Registered webhook for book.deleted: {r.json()}")

# 2. List registered webhooks
r = requests.get(f"{BASE}/webhooks")
print(f"\nRegistered webhooks ({len(r.json())}):")
for wh in r.json():
    print(f"  [{wh['id']}] {wh['event']} -> {wh['url']}")

# 3. Perform CRUD — each triggers matching webhooks
time.sleep(0.2)

r = requests.post(f"{BASE}/books", json={"title": "Fahrenheit 451", "author": "Ray Bradbury"})
print(f"\nCreated book: {r.json()['title']} (id={r.json()['id']})")

time.sleep(0.3)

r = requests.put(f"{BASE}/books/1", json={"year": 2020})
print(f"Updated book 1: year -> {r.json()['year']}")

time.sleep(0.3)

r = requests.delete(f"{BASE}/books/4")
print(f"Deleted book 4")

time.sleep(0.3)

# 4. Check what the test receiver got
r = requests.get(f"{BASE}/webhook-test-receiver")
print(f"\nWebhooks received by test receiver ({len(r.json())}):")
for wh in r.json():
    print(f"  [{wh['event']}] {wh['data'].get('title', wh['data'].get('id', ''))} at {wh['timestamp'][:19]}")
