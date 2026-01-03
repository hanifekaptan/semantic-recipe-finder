"""Recipe detail page rendering."""

import streamlit as st
from api import client as api_client


def render_detail(recipe):
    """Render recipe detail panel in scrollable container.
    
    Fetches full recipe data from API and delegates rendering
    to the recipe_detail component.
    
    Args:
        recipe: Recipe dict with at least recipe_id or id field
    """
    recipe_id = recipe.get("recipe_id") or recipe.get("id")
    full_detail = api_client.get_recipe(recipe_id)
    
    container = st.container(height=600)
    with container:
        from components import recipe_detail as recipe_detail_comp
        if full_detail:
            recipe_detail_comp.render(full_detail)
        else:
            st.error("Recipe details could not be loaded.")