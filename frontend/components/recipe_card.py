"""Recipe card component for displaying recipe summaries."""

import streamlit as st
from utils import utility


def render(recipe, on_detail_click=None):
    """Render recipe summary card with basic information.
    
    Displays recipe name, category, description preview, tags,
    and key metrics (ingredients, time, calories, rating).
    
    Args:
        recipe: Recipe dict with card data
        on_detail_click: Optional callback function called when "View Details" is clicked
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(recipe.get("name", "-"))
    st.caption(recipe.get("recipe_category", ""))

    description = recipe.get("description", "")
    if description and len(description) > 150:
        description = description[:150].rsplit(' ', 1)[0] + "..."
    st.write(description)

    tags_raw = recipe.get("keywords") or recipe.get("tags") or []
    tags = utility.normalize_to_list(tags_raw)
    if tags:
        tag_html = "".join([f"<span class=\"tag\">{t}</span>{'&nbsp;' * 10}" for t in tags[:20]])
        st.markdown(tag_html, unsafe_allow_html=True)

    st.markdown("---")
    info_cols = st.columns(4)
    info_cols[0].write(f":green_salad: **{recipe.get('n_ingredients', '-') }**\nIngredients")
    info_cols[1].write(f":alarm_clock: **{recipe.get('total_time_minutes', '-') }**\nMin")

    val = recipe.get('calories', None)
    try:
        v = float(val)
        rv = round(v, 2)
        cal = str(rv)
        if cal.endswith('.0'):
            cal = cal[:-2]
    except Exception:
        cal = '-' if val is None else str(val)
    info_cols[2].write(f":fire: **{cal}**\nkcal")

    info_cols[3].write(f":star: **{recipe.get('aggregated_rating', '-') }**\nRating")

    st.markdown("\n")
    rid = recipe.get('id') or recipe.get('recipe_id')
    if st.button("View Details", key=f"detail-{rid}"):
        if on_detail_click:
            on_detail_click(recipe)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border: 3px solid #333; margin-top: 2rem;'>", unsafe_allow_html=True)
