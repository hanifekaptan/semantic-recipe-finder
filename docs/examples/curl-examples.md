
--- FILE: examples/curl-examples.md ---
# CURL Examples

These curl examples assume the backend is running locally at `http://127.0.0.1:8000`.

1) Health check

```bash
curl -sS http://127.0.0.1:8000/health
```

2) POST search (batch)

Request the first batch (offset 0, limit 20):

```bash
curl -sS -X POST 'http://127.0.0.1:8000/search?offset=0&limit=20' -H 'Content-Type: application/json' -d '{"query":"tomato pasta"}'
```

Request the second batch (offset 20):

```bash
curl -sS -X POST 'http://127.0.0.1:8000/search?offset=20&limit=20' -H 'Content-Type: application/json' -d '{"query":"tomato pasta"}'
```

3) Recipe detail

```bash
curl -sS http://127.0.0.1:8000/recipe/123
```

4) Interactive API docs

Open `http://127.0.0.1:8000/docs` in your browser to use Swagger UI and try the endpoints interactively.

