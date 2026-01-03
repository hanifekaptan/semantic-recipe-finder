"""Main Streamlit app for Semantic Recipe Finder.

Sets up page layout and renders the search interface with
two-column layout: search results on left, recipe detail on right.
"""

import streamlit as st
from pages import search as search_page
from pages import detail as detail_page
from components import header as header_comp
from components import search_bar as search_bar_comp
from api import client as api_client
from utils import utility as utility


API_DEFAULT = "http://localhost:8000"
PAGE_SIZE = 10


def main():
    """Initialize page configuration and render UI components.
    
    Creates two-column layout:
    - Left: Search bar and results list
    - Right: Selected recipe detail view
    """
    st.set_page_config(page_title="Semantic Recipe Finder", layout="wide", initial_sidebar_state="collapsed")
    st.markdown('<style>[data-testid="stSidebar"]{display:none !important;}</style>', unsafe_allow_html=True)
    header_comp.render()

    search_clicked = search_bar_comp.render(key="query")
    left_col, right_col = st.columns([11, 9])

    with left_col:
        search_page.render_search(api_client, utility, st.session_state, page_size=PAGE_SIZE, search_clicked=search_clicked)
    with right_col:
        sel = st.session_state.get("selected_recipe")
        if sel:
            detail_page.render_detail(sel)
        else:
            st.info("Select a recipe to view details.")


if __name__ == "__main__":
    main()
