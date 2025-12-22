import { useState, useCallback, useRef } from 'react';
import type { FrontendSearchResult } from '../types/index.types';
import { searchRecipes } from '../api/recipeService';

export default function useRecipes(initialLimit = 20) {
    const [query, setQuery] = useState('');
    const [recipes, setRecipes] = useState<FrontendSearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [loadingMore, setLoadingMore] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [offset, setOffset] = useState(0);
    const [limit] = useState(initialLimit);
    const [totalCount, setTotalCount] = useState<number | null>(null);
    const currentQueryRef = useRef(query);
    const inFlightRef = useRef(false);
    // track the offset used for requests separately from the number of
    // unique items currently displayed. This prevents overlap when the
    // server returns duplicates or fewer unique items than requested.
    const requestOffsetRef = useRef(0);

    const _doSearch = useCallback(async (reset: boolean) => {
        if (reset) {
            setLoading(true);
            setError(null);
            setOffset(0);
            setTotalCount(null);
        } else {
            setLoadingMore(true);
        }

        try {
            // prevent concurrent calls
            if (!reset && inFlightRef.current) {
                console.debug('[hook] _doSearch skipped due to inFlight');
                return;
            }
            inFlightRef.current = true;
            const requestOffset = reset ? 0 : requestOffsetRef.current;
            console.debug('[hook] _doSearch start', { reset, query, requestOffset, limit });
            let resp = await searchRecipes({ query }, { expand: true, offset: requestOffset, limit });
            let results = resp.results || [];
            console.debug('[hook] _doSearch response', { returned: results.length, total_count: resp.total_count, resp_offset: resp.offset, resp_limit: resp.limit, requestOffset: requestOffsetRef.current });

            // If the server returned a block with zero unique items (all duplicates),
            // advance the request offset and retry a few times to find new items.
            let attempts = 0;
            const maxAttempts = 3;
            while (!reset && attempts < maxAttempts) {
                const existingIds = new Set(recipes.map((p) => p.id));
                const unique = results.filter((r) => !existingIds.has(r.id));
                if (unique.length > 0) break;
                attempts += 1;
                console.warn('[hook] fetched block contained only duplicates, advancing requestOffset and retrying', { attempt: attempts, requestOffset: requestOffsetRef.current });
                requestOffsetRef.current = requestOffsetRef.current + limit;
                resp = await searchRecipes({ query }, { expand: true, offset: requestOffsetRef.current, limit });
                results = resp.results || [];
                console.debug('[hook] retry response', { returned: results.length, resp_offset: resp.offset });
            }

            if (reset) {
                // dedupe results by id just in case backend returned duplicates
                const seen = new Set<number>();
                const deduped = results.filter((r) => (seen.has(r.id) ? false : (seen.add(r.id), true)));
                setRecipes(deduped);
                setOffset(deduped.length);
                // ensure request offset advances so next loadMore requests the
                // following block instead of re-requesting the same first block
                requestOffsetRef.current = deduped.length;
            } else {
                // append deduped results and update displayed offset by
                // number of unique items actually added
                setRecipes((prev) => {
                    const existing = new Set(prev.map((p) => p.id));
                    const toAdd = results.filter((r) => !existing.has(r.id));
                    if (toAdd.length !== results.length) {
                        console.warn('[hook] Duplicate items detected and removed', { attempted: results.length, added: toAdd.length });
                    }
                    // update requestOffsetRef so next request starts after
                    // the block we just requested
                    requestOffsetRef.current = requestOffsetRef.current + limit;
                    // update displayed offset based on actually added items
                    setOffset((prev) => prev + toAdd.length);
                    return [...prev, ...toAdd];
                });
                // if there were no existing items (prev length 0) the above
                // setRecipes updater also handled offset; ensure requestOffset
                // still advances when nothing was added
                if (results.length === 0) requestOffsetRef.current = requestOffsetRef.current + limit;
            }
            if (resp.total_count !== undefined) setTotalCount(resp.total_count);
        } catch (e: any) {
            console.error('[hook] _doSearch error', e);
            setError(e?.message || 'Search failed');
        } finally {
            inFlightRef.current = false;
            setLoading(false);
            setLoadingMore(false);
        }
    }, [query, offset, limit]);

    const search = useCallback(() => {
        currentQueryRef.current = query;
        _doSearch(true);
    }, [query, _doSearch]);

    const loadMore = useCallback(() => {
        if (loading || loadingMore) return;
        if (totalCount !== null && offset >= totalCount) return;
        _doSearch(false);
    }, [loading, loadingMore, totalCount, offset, _doSearch]);

    const reset = useCallback(() => {
        setRecipes([]);
        setOffset(0);
        setTotalCount(null);
        setError(null);
    }, []);

    const hasMore = totalCount === null ? true : offset < totalCount;

    return { query, setQuery, recipes, loading, loadingMore, error, search, loadMore, reset, hasMore, offset, limit };
}
