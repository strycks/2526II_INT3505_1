import requests

BASE = "http://127.0.0.1:5001/books"

# GET all — notice the links in the response
r = requests.get(BASE)
body = r.json()
print("=== GET /books ===")
print(f"Root links: {body['links']}")
print(f"First book: {body['data'][0]}")
print()

# Follow the "self" link of the first book
self_link = body["data"][0]["links"][0]["href"]  # rel="self", GET
r = requests.get(f"http://127.0.0.1:5001{self_link}")
print(f"=== GET {self_link} ===")
print(r.json())
print()

# Create — use the "create" link
create_link = next(l for l in body["links"] if l["rel"] == "create")
r = requests.post(f"http://127.0.0.1:5001{create_link['href']}",
                   json={"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953})
created = r.json()
print(f"=== POST {create_link['href']} (create) ===")
print(created)
print()

# Update — use the "update" link from the created book
update_link = next(l for l in created["links"] if l["rel"] == "update")
bid = created["data"]["id"]
r = requests.put(f"http://127.0.0.1:5001{update_link['href']}",
                  json={"genre": "Dystopian"})
print(f"=== PUT {update_link['href']} (update book {bid}) ===")
print(r.json())
print()

# Delete — use the "delete" link
delete_link = next(l for l in created["links"] if l["rel"] == "delete")
r = requests.delete(f"http://127.0.0.1:5001{delete_link['href']}")
print(f"=== DELETE {delete_link['href']} (delete book {bid}) ===")
print(r.json())
print()

# Verify deletion
r = requests.get(BASE)
print(f"=== GET /books (after delete) ===")
print(f"Remaining books: {len(r.json()['data'])}")
