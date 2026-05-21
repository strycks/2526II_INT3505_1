import requests

BASE = "http://127.0.0.1:5000/books"

# POST - create books
for b in [
    {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi"},
    {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian"},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian"},
    {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "Sci-Fi"},
]:
    r = requests.post(BASE, json=b)
    print(f"POST {b['title']} -> {r.status_code} {r.json()}")

# GET all
r = requests.get(BASE)
print(f"\nGET all -> {r.status_code} ({len(r.json())} books)")

# GET with search
r = requests.get(BASE, params={"q": "dune"})
print(f"\nGET search 'dune' -> {r.status_code} {[b['title'] for b in r.json()]}")

# GET with filter
r = requests.get(BASE, params={"genre": "Sci-Fi"})
print(f"GET filter Sci-Fi -> {r.status_code} {[b['title'] for b in r.json()]}")

# GET with filter + search
r = requests.get(BASE, params={"genre": "Dystopian", "q": "1984"})
print(f"GET Dystopian + '1984' -> {r.status_code} {[b['title'] for b in r.json()]}")

# GET single
r = requests.get(f"{BASE}/1")
print(f"\nGET /1 -> {r.status_code} {r.json()}")

# PUT update
r = requests.put(f"{BASE}/1", json={"year": 2021, "genre": "Sci-Fi/Fantasy"})
print(f"PUT /1 -> {r.status_code} {r.json()}")

# DELETE
r = requests.delete(f"{BASE}/4")
print(f"\nDELETE /4 -> {r.status_code} {r.json()}")

r = requests.get(BASE)
print(f"GET all after delete -> {r.status_code} ({len(r.json())} books)")
