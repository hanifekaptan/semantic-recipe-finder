"""Application header component."""

import streamlit as st


def render():
    """Render application title and subtitle header."""
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:28px;font-weight:700">Semantic Recipe Finder</div>
            <div style="color:#6b7280">— semantic recipe search demo</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
