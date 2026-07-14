# Python: Working with APIs and HTTP

Calling an API in Python is mostly about understanding a small loop:

1. Build the URL.
2. Add query parameters, headers, or authentication if needed.
3. Send the request.
4. Inspect the status code and headers.
5. Decode the response body.
6. Handle errors explicitly.

For most modern Python work, the default tool is `requests`.

## What an API Is

An API is an interface for interacting with another system.

For web APIs:

- the client sends an HTTP request
- the server returns an HTTP response
- the response usually contains a status code, headers, and a body

This is the core mental model behind most REST-style APIs.

## First Request

```python
import requests

response = requests.get("https://api.example.com/items")
print(response.status_code)
print(response.text)
```

Useful response attributes:

- `response.status_code`
- `response.text`
- `response.headers`
- `response.url`
- `response.json()`

## `urllib` vs `requests`

Python ships with `urllib`, but in day-to-day data work `requests` is usually easier to read.

```python
from urllib.request import urlopen

with urlopen("https://api.example.com/items") as response:
    data = response.read()
```

Compared with:

```python
import requests

response = requests.get("https://api.example.com/items")
print(response.text)
```

If there is no strong reason to stay in the standard library, `requests` is usually the cleaner choice.

## URL Structure and Endpoints

An API URL identifies a resource or collection of resources.

```python
https://api.example.com/albums
https://api.example.com/albums/42
https://api.example.com/albums/42/tracks
```

Think of it like:

- base URL: the service
- path: the resource
- query string: filters or options

## Query Parameters

You can append query parameters manually, but `params=` is safer.

```python
query_params = {
    "artist": "Deep Purple",
    "limit": 10,
}

response = requests.get(
    "https://api.example.com/albums",
    params=query_params,
)

print(response.url)
```

- `params=` handles encoding for you
- the final URL is visible via `response.url`
- use query parameters for filtering, sorting, paging, or search terms

## Common HTTP Verbs

For simple REST APIs, the verbs you use most often are:

- `GET`: retrieve a resource
- `POST`: create a resource
- `PUT`: replace or update a resource
- `DELETE`: remove a resource

Example:

```python
requests.get("https://api.example.com/items/42")
requests.post("https://api.example.com/items", data={"name": "new item"})
requests.put("https://api.example.com/items/42", data={"name": "updated item"})
requests.delete("https://api.example.com/items/42")
```

In practice:

- `GET` is the most common for data retrieval
- `POST` is common for creation and sometimes search-style endpoints
- some APIs use `PATCH` for partial updates instead of `PUT`

## Sending JSON

If the API expects JSON, prefer `json=` over manually serializing payloads into `data=`.

```python
playlist = {
    "name": "Road Trip",
    "tracks": [1, 2, 3],
}

response = requests.post(
    "https://api.example.com/playlists",
    json=playlist,
)
```

Why `json=` is useful:

- it serializes the Python object to JSON
- it sets the request `Content-Type` to `application/json`

You can inspect the prepared request if needed:

```python
request = response.request
print(request.headers["Content-Type"])
```

## Reading JSON Responses

Many APIs return JSON.

```python
response = requests.get(
    "https://api.example.com/lyrics",
    headers={"Accept": "application/json"},
)

data = response.json()
```

Useful distinction:

- `response.text` gives the raw text body
- `response.json()` parses the body into Python objects

If you need to encode or decode JSON manually:

```python
import json

string = json.dumps(data)
decoded = json.loads(string)
```

## Headers

Headers let the client and server negotiate how data should be sent.

```python
response = requests.get(
    "https://api.example.com/items",
    headers={"Accept": "application/json"},
)

print(response.headers.get("Content-Type"))
```

Common header uses:

- `Accept`: what response format you want
- `Authorization`: how you authenticate
- `Content-Type`: what format the request body uses

### Content Negotiation

A common pattern is:

- client sends `Accept: application/json`
- server responds with `Content-Type: application/json`

This is a clean way to request machine-readable output explicitly.

## Authentication Patterns

The API documentation always wins here, but a few patterns appear repeatedly.

### Basic Auth

```python
requests.get(
    "https://api.example.com",
    auth=("username", "password"),
)
```

`requests` will generate the `Authorization` header for you.

### API Key in Query Parameters

```python
params = {"access_token": "abc123"}
requests.get("https://api.example.com/albums", params=params)
```

This works, but many APIs now prefer header-based authentication.

### Bearer Token

```python
headers = {"Authorization": "Bearer abc123"}
requests.get("https://api.example.com/albums", headers=headers)
```

This is one of the most common modern patterns.

## Status Codes

Every HTTP response includes a numeric status code.

High-level categories:

- `1xx`: informational
- `2xx`: success
- `3xx`: redirection
- `4xx`: client-side errors
- `5xx`: server-side errors

Frequently encountered examples:

- `200 OK`
- `401 Unauthorized`
- `404 Not Found`
- `429 Too Many Requests`
- `500 Internal Server Error`
- `502 Bad Gateway`

Helpful mental model:

- `4xx` usually means fix the request
- `5xx` usually means the server or upstream service failed

## Checking Errors Explicitly

You can inspect the status code yourself:

```python
response = requests.get("https://api.example.com/items/42")

if response.status_code >= 400:
    print("Request failed")
```

Or compare against named codes:

```python
response.status_code == requests.codes.ok
response.status_code == requests.codes.not_found
```

## `raise_for_status()` Pattern

For most scripts, `raise_for_status()` is the cleanest default.

```python
import requests
from requests.exceptions import ConnectionError, HTTPError

try:
    response = requests.get("https://api.example.com/albums")
    response.raise_for_status()
    data = response.json()
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
```

Why this is good:

- success path stays simple
- HTTP failures become exceptions automatically
- network failures and server-side response failures can be handled separately

## Request / Response Anatomy

At a high level, an HTTP exchange contains:

Request:

- method
- URL
- headers
- optional body

Response:

- status code
- headers
- optional body

When debugging API calls, these are the first things to inspect.

## Practical Checklist

Before blaming the API, verify:

- Is the URL correct?
- Are the query parameters encoded correctly?
- Did you use the right HTTP method?
- Are the required headers present?
- Is authentication attached in the format the docs expect?
- Did the response actually return JSON before calling `.json()`?
- Is the error a `4xx` problem you must fix, or a `5xx` problem from the server?

## Key Takeaways

- Use `requests` as the default tool for web APIs in Python.
- Prefer `params=` for query strings and `json=` for JSON request bodies.
- Inspect `status_code`, `headers`, and `response.json()` as separate concerns.
- Treat authentication style as API-specific; common patterns are Basic auth and Bearer tokens.
- Default to `raise_for_status()` in scripts so failures are explicit instead of silent.
