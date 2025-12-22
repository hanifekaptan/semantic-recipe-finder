import React from 'react';
import SearchBar from '../../components/search/SearchBar';
import RecipeList from '../../components/recipe/RecipeList';
import RecipeDetailModal from '../../components/recipe/RecipeDetailModal';
import useRecipes from '../../hooks/useRecipes';
import { getRecipeById } from '../../api/recipeService';
import type { FrontendRecipeDetail } from '../../types/index.types';

export default function HomePage() {
    const { query, setQuery, recipes, loading, loadingMore, error, search, loadMore, hasMore } = useRecipes(50);
    const [selectedId, setSelectedId] = React.useState<number | null>(null);
    const [selectedRecipe, setSelectedRecipe] = React.useState<FrontendRecipeDetail | null>(null);

    // Use IntersectionObserver on a sentinel element to trigger loading.
    // Only trigger if the user has scrolled past `threshold` new items
    // since the last load to avoid rapid repeated loads.
    const sentinelRef = React.useRef<HTMLDivElement | null>(null);
    const lastTriggerCountRef = React.useRef(0);
    const threshold = 20; // load more after ~20 items have been seen

    React.useEffect(() => {
        const el = sentinelRef.current;
        if (!el) return;
        const obs = new IntersectionObserver((entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    const seenSinceLast = recipes.length - lastTriggerCountRef.current;
                    if (hasMore && !loading && !loadingMore && seenSinceLast >= threshold) {
                        lastTriggerCountRef.current = recipes.length;
                        loadMore();
                    }
                }
            }
        }, { root: null, rootMargin: '0px', threshold: 0.1 });
        obs.observe(el);
        return () => obs.disconnect();
    }, [recipes.length, hasMore, loading, loadingMore, loadMore]);

    return (
        <main className="page-root">
            <div className="centered-container">
                <h1>Semantic Recipe Finder</h1>
                <div style={{ marginBottom: 24 }}>
                    <SearchBar value={query} onChange={setQuery} onSearch={() => { search(); }} />
                </div>
                {loading && <div>Loading...</div>}
                {error && <div style={{ color: 'red' }}>{error}</div>}
                <RecipeList recipes={recipes} onOpen={(id) => {
                    setSelectedId(id);
                    setSelectedRecipe(null);
                    getRecipeById(id).then((d) => setSelectedRecipe(d)).catch(() => setSelectedRecipe(null));
                }} />

                {loadingMore && <div>Loading more...</div>}
                {!hasMore && recipes.length > 0 && <div>No more recipes.</div>}
                <div ref={sentinelRef} style={{ height: 1 }} />

                <RecipeDetailModal open={!!selectedId} recipe={selectedRecipe} onClose={() => { setSelectedId(null); setSelectedRecipe(null); }} />
            </div>
        </main>
    );
}
