from app.models.recipe_detail import RecipeDetail

def test_recipe_detail_model_basic():
    data = {"recipe_id": 1, "name": "X"}
    rd = RecipeDetail(**data)
    assert rd.recipe_id == 1
    assert rd.name == "X"