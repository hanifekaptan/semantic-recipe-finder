import type { SearchQuery, FrontendSearchResult, SearchResponseBackend, FrontendRecipeDetail } from "../types/index.types";
import { mapRecipeCardToFrontend, mapRecipeDetailToFrontend } from "../types/index.types";

const BASE_URL =
    import.meta.env.VITE_API_BASE_URL

type SearchOptions = { expand?: boolean; timeoutMs?: number; offset?: number; limit?: number };

const detailCache = new Map<number, FrontendRecipeDetail | null>();

async function fetchWithTimeout(input: RequestInfo, init?: RequestInit, timeoutMs = 8000) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const res = await fetch(input, { signal: controller.signal, ...init } as RequestInit);
        return res;
    } finally {
        clearTimeout(id);
    }
}

export async function searchRecipes(
    payload: SearchQuery,
    { expand = false, timeoutMs = 8000, offset = 0, limit = 20 }: SearchOptions = {}
): Promise<{ results: FrontendSearchResult[]; total_count?: number; offset?: number; limit?: number }> {

    const url = new URL(`${BASE_URL}/search`);
    url.searchParams.set('offset', String(offset));
    url.searchParams.set('limit', String(limit));

    const res = await fetchWithTimeout(url.toString(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    }, timeoutMs);

    if (res.status === 503) {
        const retry = res.headers.get('Retry-After') || '30';
        throw new Error(`Search service warming up; try again in ${retry}s`);
    }

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Search API error: ${res.status} ${text}`);
    }

    const raw = await res.json();

    if (Array.isArray(raw)) {
        const minimal = (raw as any[]).map((rc) => mapRecipeCardToFrontend(rc as any));
        return { results: minimal };
    }

    const data: SearchResponseBackend = raw as SearchResponseBackend;

    const minimalResults: FrontendSearchResult[] = data.search_results.map((result) => ({
        id: result.recipe_id,
        score: result.similarity_score,
    }));

    let finalResults: FrontendSearchResult[] = minimalResults;
    if (expand) {
        const details = await Promise.all(
            minimalResults.map((r) => getRecipeById(r.id, { timeoutMs }))
        );

        finalResults = details.map((d: FrontendRecipeDetail | null, i: number) => {
            if (!d) return minimalResults[i];
            return {
                id: d.id,
                title: d.title,
                description: d.description,
                ingredients: d.ingredients,
                score: d.score ?? minimalResults[i].score,
                keywords: d.keywords,
                category: d.category,
                total_time_minutes: d.total_time_minutes,
                n_ingredients: d.n_ingredients,
                calories: d.calories,
                aggregated_rating: d.aggregated_rating,
            } as FrontendSearchResult;
        });
    }

    return { results: finalResults, total_count: data.total_count, offset: data.offset, limit: data.limit };
}

export async function getRecipeById(id: number, { timeoutMs = 8000 }: { timeoutMs?: number } = {}): Promise<FrontendRecipeDetail | null> {
    if (detailCache.has(id)) return detailCache.get(id) ?? null;

    const res = await fetchWithTimeout(`${BASE_URL}/recipe/${id}`, undefined, timeoutMs);
    if (res.status === 503) {
        const retry = res.headers.get('Retry-After') || '30';
        throw new Error(`Search service warming up; try again in ${retry}s`);
    }
    if (!res.ok) {
        if (res.status === 404) return null;
        const text = await res.text();
        throw new Error(`Recipe detail API error: ${res.status} ${text}`);
    }

    const data = await res.json();

    const mapped = mapRecipeDetailToFrontend(data as any);
    detailCache.set(id, mapped);
    return mapped;
}

export function clearRecipeCache() {
    detailCache.clear();
}