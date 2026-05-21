import requests

BASE = "http://127.0.0.1:5001/books"

# POST - create books
for b in [
    {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi"},
    {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian"},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian"},
    {"title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "Sci-Fi"},
]:
    r = requests.post(BASE, json=b)
    print(f"POST {b['title']} -> {r.status_code} {r.json()}")

# GET all (paginated with metadata)
r = requests.get(BASE)
body = r.json()
print(f"\nGET all -> page={body['page']}, per_page={body['per_page']}, total={body['total']}")
print(f"Books on this page: {[b['title'] for b in body['data']]}")

# GET with search
r = requests.get(BASE, params={"q": "dune"})
print(f"\nGET search 'dune' -> {[b['title'] for b in r.json()['data']]}")

# GET with filter
r = requests.get(BASE, params={"genre": "Sci-Fi"})
print(f"GET filter Sci-Fi -> {[b['title'] for b in r.json()['data']]}")

# GET with filter + search
r = requests.get(BASE, params={"genre": "Dystopian", "q": "1984"})
print(f"GET Dystopian + '1984' -> {[b['title'] for b in r.json()['data']]}")

# GET sorted by year descending
r = requests.get(BASE, params={"sort_by": "year", "order": "desc", "per_page": 20})
titles = [f"{b['title']} ({b['year']})" for b in r.json()["data"]]
print(f"\nGET sort_by=year&order=desc -> {titles}")

# GET paginated (page 1, per_page 2)
r = requests.get(BASE, params={"per_page": 2, "page": 1})
body = r.json()
print(f"\nGET per_page=2&page=1 -> page={body['page']}/{body['total_pages']}, "
      f"got {len(body['data'])} books: {[b['title'] for b in body['data']]}")

r = requests.get(BASE, params={"per_page": 2, "page": 2})
body = r.json()
print(f"GET per_page=2&page=2 -> page={body['page']}/{body['total_pages']}, "
      f"got {len(body['data'])} books: {[b['title'] for b in body['data']]}")

# GET single
r = requests.get(f"{BASE}/1")
print(f"\nGET /1 -> {r.status_code} {r.json()}")

# PUT update
r = requests.put(f"{BASE}/1", json={"year": 2021, "genre": "Sci-Fi/Fantasy"})
print(f"PUT /1 -> {r.status_code} {r.json()}")

# DELETE
r = requests.delete(f"{BASE}/4")
print(f"\nDELETE /4 -> {r.status_code} {r.json()}")

r = requests.get(BASE, params={"per_page": 20})
body = r.json()
print(f"GET all after delete -> {body['total']} books remaining")
