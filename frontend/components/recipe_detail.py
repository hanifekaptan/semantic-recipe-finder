"""Recipe detail component for full recipe view."""

import streamlit as st
import plotly.graph_objects as go
from utils import utility


def _donut(perc: float, label: str, grams: float):
    """Render nutrition donut chart.
    
    Args:
        perc: Percentage value (0-100)
        label: Nutrition label (e.g., 'Fat', 'Protein')
        grams: Gram amount to display below chart
    """
    perc = max(0, min(100, (perc or 0)))
    fig = go.Figure(
        data=[
            go.Pie(
                values=[perc, 100 - perc],
                hole=0.6,
                marker_colors=["#4CAF50", "#e9ecef"],
                hoverinfo="none",
                textinfo="none",
            )
        ]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), width=140, height=140)
    fig.add_annotation(x=0.5, y=0.5, text=f"{perc:.2f}%", showarrow=False, font=dict(size=16))
    st.plotly_chart(fig, width='content')
    st.markdown(f"**{label}**")
    try:
        g = float(grams)
        st.markdown(f"{g:.2f} g")
    except Exception:
        st.markdown(f"{grams}")


def render(recipe):
    """Render complete recipe detail view.
    
    Displays full recipe information including name, description, tags,
    ingredients, instructions, and nutrition charts.
    
    Args:
        recipe: Dict with complete recipe data
    """
    if not isinstance(recipe, dict):
        st.error(f"Invalid data type for recipe: {type(recipe)}")
        st.write(recipe)
        return

    st.title(recipe.get("name", "-"))
    st.caption(recipe.get("recipe_category", ""))
    st.write(recipe.get("description", ""))

    tags_raw = recipe.get("keywords") or recipe.get("tags") or []
    tags = utility.normalize_to_list(tags_raw)
    if tags:
        tag_html = "".join([f"<span class=\"tag\">{t}</span>{'&nbsp;' * 10}" for t in tags[:20]])
        st.markdown(tag_html, unsafe_allow_html=True)

    st.markdown("---")
    cols = st.columns(4)
    cols[0].write(f":green_salad: **{recipe.get('n_ingredients', '-') }**\nIngredients")
    cols[1].write(f":alarm_clock: **{recipe.get('total_time_minutes', '-') }**\nMin")

    val = recipe.get('calories', None)
    try:
        v = float(val)
        rv = round(v, 2)
        cal = str(rv)
        if cal.endswith('.0'):
            cal = cal[:-2]
    except Exception:
        cal = '-' if val is None else str(val)
    cols[2].write(f":fire: **{cal}**\nkcal")

    cols[3].write(f":star: **{recipe.get('aggregated_rating', '-') }**\nRating")

    st.markdown("---")
    st.subheader("Ingredients")
    ingredients_raw = recipe.get("ingredients") or []
    ingredients = utility.normalize_to_list(ingredients_raw)
    if ingredients:
        for ing in ingredients:
            st.write(f"- {ing}")
    else:
        st.write("No ingredients listed.")

    st.markdown("---")
    st.subheader("Instructions")
    instructions_raw = recipe.get("recipe_instructions") or []
    instructions = utility.normalize_to_list(instructions_raw)
    if instructions:
        for i, ins in enumerate(instructions):
            st.checkbox(ins, key=f"ins-{recipe.get('id')}-{i}")
    else:
        st.write("No instructions available.")

    st.markdown("---")
    st.subheader("Nutrition (%)")
    nuts = [
        (float(recipe.get("fat_content_perc") or 0), "Fat", recipe.get("fat_content", "-")),
        (float(recipe.get("protein_content_perc") or 0), "Protein", recipe.get("protein_content", "-")),
        (float(recipe.get("sugar_content_perc") or 0), "Sugar", recipe.get("sugar_content", "-")),
        (float(recipe.get("carbohydrate_content_perc") or 0), "Carb", recipe.get("carbohydrate_content", "-")),
    ]
    cols = st.columns(4)
    for c, (perc, label, grams) in zip(cols, nuts):
        with c:
            _donut(perc, label, grams)
