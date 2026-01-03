"""Search input component for recipe queries."""

import streamlit as st


def render(key="query", placeholder="What are you looking for?"):
    """Render search input field and button.
    
    Args:
        key: Session state key for storing input value
        placeholder: Input field placeholder text
        
    Returns:
        True when search button is clicked, False otherwise
    """
    st.text_input(placeholder, key=key)
    return st.button("Search", key=f"{key}_button")