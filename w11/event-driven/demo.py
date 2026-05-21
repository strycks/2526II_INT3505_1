import requests
import time

BASE = "http://127.0.0.1:5002"

# After seed, check search index was populated by events
r = requests.get(f"{BASE}/events/search-index")
print("=== Search Index (built from seed events) ===")
print(r.json())

r = requests.get(f"{BASE}/events/audit")
print(f"\n=== Audit Log ({len(r.json())} entries from seed) ===")

# Create a book — event fires
r = requests.post(f"{BASE}/books", json={"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953})
print(f"\n=== POST (creates book.id={r.json()['id']}) ===")

time.sleep(0.1)  # let async handlers finish

# Check audit log updated
r = requests.get(f"{BASE}/events/audit")
print(f"\n=== Audit Log after POST ({len(r.json())} entries) ===")
print(f"Last event: {r.json()[-1]['event']} -> {r.json()[-1]['data']['title']}")

# Update a book — event fires
r = requests.put(f"{BASE}/books/1", json={"genre": "Sci-Fi/Fantasy"})
print(f"\n=== PUT book/1 ===")

time.sleep(0.1)

# Check search index still intact
r = requests.get(f"{BASE}/events/search-index")
print(f"\n=== Search Index (all IDs should still be present) ===")
print(r.json())

# Delete a book — event fires
r = requests.delete(f"{BASE}/books/4")
print(f"\n=== DELETE book/4 ===")

time.sleep(0.1)

# Verify search index updated
r = requests.get(f"{BASE}/events/search-index")
print(f"\n=== Search Index after delete (id=4 should be gone) ===")
print(r.json())
