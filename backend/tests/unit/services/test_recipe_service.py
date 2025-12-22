import numpy as np
from app.services.recipe_service import RecipeService

def test_get_cards_orders(sample_df):
    svc = RecipeService(df=sample_df.set_index("recipe_id", drop=False))
    ids = np.array([10, 12], dtype=np.int64)
    sims = np.array([0.8, 0.5], dtype=np.float32)
    cards = svc.get_cards_for_ids(ids, sims)
    assert cards[0]["recipe_id"] == 10
    assert cards[1]["recipe_id"] == 12

def test_keywords_normalized(sample_df):
    svc = RecipeService(df=sample_df.set_index("recipe_id", drop=False))
    ids = [10,11,12]
    sims = [0.9,0.8,0.1]
    cards = svc.get_cards_for_ids(ids, sims)
    for c in cards:
        assert isinstance(c.get("keywords", []), list)
