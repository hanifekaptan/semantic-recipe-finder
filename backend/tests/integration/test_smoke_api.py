def test_health_endpoint(client_with_preloaded_state):
    client = client_with_preloaded_state
    r = client.get("/health")
    assert r.status_code == 200


def test_recipe_detail_endpoint(client_with_preloaded_state):
    client = client_with_preloaded_state
    # using one of sample ids 10
    r = client.get("/recipe/10")
    assert r.status_code == 200
    j = r.json()
    assert "recipe_id" in j


def test_search_smoke(client_with_preloaded_state):
    client = client_with_preloaded_state
    payload = {"query": "something", "k": 2}
    r = client.post("/search", json=payload)
    assert r.status_code == 200
    j = r.json()
    # API returns `search_results` by design
    assert isinstance(j.get("search_results"), list)
