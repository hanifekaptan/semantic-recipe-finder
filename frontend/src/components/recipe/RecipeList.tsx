import RecipeCard from './RecipeCard';
import type { FrontendSearchResult } from '../../types/index.types';

type Props = {
    recipes: FrontendSearchResult[];
    onOpen: (id: number) => void;
};

export default function RecipeList({ recipes, onOpen }: Props) {
    if (!recipes.length) return <div>No recipes found.</div>;
    return (
        <div className="recipe-list" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {recipes.map(r => (
                <div key={r.id} style={{ width: '100%' }}>
                    <RecipeCard recipe={r} onOpen={onOpen} />
                </div>
            ))}
        </div>
    );
}
