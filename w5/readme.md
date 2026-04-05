# Comparision between Cursor-based and Page-based Pagination

## Implementation

**GET** method in [/api/v1/books](/api/v1/books) is implemented using page-based.  
**GET** method in [/api/v1/users](/api/v1/users) is implemented using cursor-based.

Both database contains one million records.

## Result
```
Elapsed time: 7.814817 seconds
192.168.1.6 - - [03/Apr/2026 18:58:22] "GET /api/v1/books?page=100000&per_page=10 HTTP/1.1" 200 -

Elapsed time: 0.000256 seconds
192.168.1.6 - - [03/Apr/2026 18:58:32] "GET /api/v1/users?after=999990&limit=10 HTTP/1.1" 200 -
```

We can clearly see that page-based one is much slower with large number of records.