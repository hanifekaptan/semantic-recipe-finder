"""Search results page with pagination and card rendering."""

import streamlit as st


def render_search(api_client, utils, page_state, page_size=10, search_clicked=False, **kwargs):
    """Render search results panel with infinite scroll.
    
    Manages search results in session state and handles pagination.
    When a recipe card is clicked, fetches full detail from API and
    stores in session state for the detail panel.
    
    Args:
        api_client: API client module for backend calls
        utils: Utility module for data normalization
        page_state: Streamlit session state
        page_size: Number of results per page
        search_clicked: Whether search button was clicked
    """
    if "results" not in page_state:
        page_state.results = []
        page_state.offset = 0
        page_state.finished = False

    container = st.container(height=600)
    with container:
        query = page_state.get("query", "")

        if search_clicked and query.strip():
            page_state.offset = 0
            page_state.results = []
            page_state.finished = False
            resp = api_client.search(query, offset=page_state.offset, limit=page_size)
            items = []
            if isinstance(resp, dict):
                items = resp.get("search_results", [])
            elif isinstance(resp, list):
                items = resp

            results = []
            for it in items:
                rid = it.get("recipe_id") if isinstance(it, dict) else None
                score = it.get("similarity_score") if isinstance(it, dict) else None
                if rid is None:
                    continue
                card = it.get("card") if isinstance(it, dict) else None
                if card:
                    card["similarity_score"] = score
                    results.append(card)
                else:
                    detail = api_client.get_recipe(rid)
                    if isinstance(detail, dict):
                        detail["similarity_score"] = score
                        results.append(detail)
                    else:
                        results.append({"id": rid, "recipe_id": rid, "similarity_score": score})

            page_state.results.extend(results)
            if len(results) < page_size:
                page_state.finished = True

        if not page_state.results:
            st.info("No search performed yet — enter a query above and click Search.")
        else:
            for r in page_state.results:
                try:
                    from components import recipe_card as recipe_card_comp
                    rid = r.get('recipe_id') or r.get('id')

                    def create_detail_callback(recipe_id):
                        def callback(card):
                            full_detail = api_client.get_recipe(recipe_id)
                            if full_detail:
                                page_state["selected_recipe"] = full_detail
                            else:
                                page_state["selected_recipe"] = card
                        return callback
                    
                    recipe_card_comp.render(r, on_detail_click=create_detail_callback(rid))
                except Exception:
                    st.write(r)

            if not page_state.finished:
                if st.button("Load more", key="load-more"):
                    page_state.offset += page_size
                    resp = api_client.search(query, offset=page_state.offset, limit=page_size)
                    items = []
                    if isinstance(resp, dict):
                        items = resp.get("search_results", [])
                    elif isinstance(resp, list):
                        items = resp
                    results = []
                    for it in items:
                        rid = it.get("recipe_id") if isinstance(it, dict) else None
                        score = it.get("similarity_score") if isinstance(it, dict) else None
                        if rid is None:
                            continue
                        card = it.get("card") if isinstance(it, dict) else None
                        if card:
                            card["similarity_score"] = score
                            results.append(card)
                        else:
                            detail = api_client.get_recipe(rid)
                            if isinstance(detail, dict):
                                detail["similarity_score"] = score
                                results.append(detail)
                            else:
                                results.append({"id": rid, "recipe_id": rid, "similarity_score": score})
                    page_state.results.extend(results)
                    if len(results) < page_size:
                        page_state.finished = True
