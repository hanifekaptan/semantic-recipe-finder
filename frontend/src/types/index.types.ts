export interface RecipeCard {
    recipe_id: number;
    name?: string | null;
    description?: string | null;
    recipe_category?: string | null;
    keywords?: string[];
    n_ingredients?: number | null;
    total_time_minutes?: number | null;
    calories?: number | null;
    aggregated_rating?: number | null;
}

export interface RecipeDetail {
    recipe_id: number;
    name?: string | null;
    description?: string | null;
    recipe_category?: string | null;
    keywords?: string[];
    ingredients?: string[];
    fat_content?: string | null;
    protein_content?: string | null;
    sugar_content?: string | null;
    carbohydrate_content?: string | null;
    fat_content_perc?: number | null;
    protein_content_perc?: number | null;
    sugar_content_perc?: number | null;
    carbohydrate_content_perc?: number | null;
    n_ingredients?: number | null;
    total_time_minutes?: number | null;
    calories?: number | null;
    aggregated_rating?: number | null;
    recipe_instructions?: string | null;
    similarity_score?: number | null;
}

export interface SearchResultBackend {
    recipe_id: number;
    similarity_score: number;
}

export interface SearchResponseBackend {
    search_results: SearchResultBackend[];
    total_count?: number;
    offset?: number;
    limit?: number;
}

export interface SearchQuery {
    query: string;
}

export interface FrontendSearchResult {
    id: number;
    title?: string;
    description?: string;
    ingredients?: string[];
    score?: number;
    keywords?: string[];
    category?: string;
    total_time_minutes?: number;
    n_ingredients?: number;
    calories?: number;
    aggregated_rating?: number;
}

export interface FrontendRecipeDetail {
    id: number;
    title?: string;
    description?: string;
    keywords?: string[];
    ingredients?: string[];
    instructions?: string;
    score?: number;
    n_ingredients?: number;
    nutrition_content?: {
        fat?: string | null;
        protein?: string | null;
        sugar?: string | null;
        carbohydrate?: string | null;
    };
    nutrition_percents?: {
        fat?: number | null;
        protein?: number | null;
        sugar?: number | null;
        carbohydrate?: number | null;
    };
    total_time_minutes?: number;
    calories?: number;
    aggregated_rating?: number;
    category?: string;
}

export function mapRecipeCardToFrontend(rc: RecipeCard): FrontendSearchResult {
    return {
        id: rc.recipe_id,
        title: rc.name ?? rc.description ?? undefined,
        description: rc.description ?? undefined,
        ingredients: undefined,
        score: rc.aggregated_rating ?? undefined,
        keywords: rc.keywords ?? [],
        category: rc.recipe_category ?? undefined,
        total_time_minutes: rc.total_time_minutes ?? undefined,
        n_ingredients: rc.n_ingredients ?? undefined,
        calories: (rc.calories !== undefined && rc.calories !== null) ? Math.round(rc.calories) : undefined,
        aggregated_rating: rc.aggregated_rating ?? undefined,
    };
}

export function mapRecipeDetailToFrontend(rd: RecipeDetail): FrontendRecipeDetail {
    return {
        id: rd.recipe_id,
        title: rd.name ?? rd.description ?? undefined,
        description: rd.description ?? undefined,
        keywords: rd.keywords ?? [],
        ingredients: rd.ingredients ?? [],
        instructions: rd.recipe_instructions ?? undefined,
        score: rd.similarity_score ?? rd.aggregated_rating ?? undefined,
        n_ingredients: rd.n_ingredients ?? undefined,
        nutrition_content: {
            fat: (() => { const v = rd.fat_content; if (v === undefined || v === null) return null; const n = typeof v === 'string' ? parseFloat(v) : Number(v); return Number.isFinite(n) ? String(n.toFixed(2)) : String(v); })(),
            protein: (() => { const v = rd.protein_content; if (v === undefined || v === null) return null; const n = typeof v === 'string' ? parseFloat(v) : Number(v); return Number.isFinite(n) ? String(n.toFixed(2)) : String(v); })(),
            sugar: (() => { const v = rd.sugar_content; if (v === undefined || v === null) return null; const n = typeof v === 'string' ? parseFloat(v) : Number(v); return Number.isFinite(n) ? String(n.toFixed(2)) : String(v); })(),
            carbohydrate: (() => { const v = rd.carbohydrate_content; if (v === undefined || v === null) return null; const n = typeof v === 'string' ? parseFloat(v) : Number(v); return Number.isFinite(n) ? String(n.toFixed(2)) : String(v); })(),
        },
        nutrition_percents: {
            fat: rd.fat_content_perc ?? null,
            protein: rd.protein_content_perc ?? null,
            sugar: rd.sugar_content_perc ?? null,
            carbohydrate: rd.carbohydrate_content_perc ?? null,
        },
        total_time_minutes: rd.total_time_minutes ?? undefined,
        calories: (rd.calories !== undefined && rd.calories !== null) ? Math.round(rd.calories) : undefined,
        aggregated_rating: rd.aggregated_rating ?? undefined,
        category: rd.recipe_category ?? undefined,
    };
}