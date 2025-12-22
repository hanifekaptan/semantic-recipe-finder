import type { FrontendSearchResult } from '../../types/index.types';
import styles from './RecipeCard.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faList, faFire } from '@fortawesome/free-solid-svg-icons';
import { faClock, faStar } from '@fortawesome/free-regular-svg-icons';

type Props = {
    recipe: FrontendSearchResult;
    onOpen?: (id: number) => void;
};

export default function RecipeCard({ recipe, onOpen }: Props) {
    const keywords = recipe.keywords ?? [];
    const visible = keywords.slice(0, 6);
    const palette = ['orange', 'yellow', 'purple', 'blue', 'green'];

    const nIngredients = (recipe as any).n_ingredients ?? (recipe.ingredients ? recipe.ingredients.length : undefined);
    const displayCalories = (recipe.calories !== undefined && recipe.calories !== null) ? Math.round(recipe.calories) : undefined;

    return (
        <div
            className={styles.card}
            role="button"
            tabIndex={0}
            onClick={() => onOpen?.(recipe.id)}
            onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen?.(recipe.id); } }}
            aria-label={`Open ${recipe.title ?? 'recipe'}`}
        >
            <div className={styles.left}>
                <div className={styles.imagePlaceholder} />
            </div>

            <div className={styles.right}>
                <div className={styles.header}>
                    <div className={styles.titleWrap}>
                        <h3 className={styles.title}>{recipe.title ?? recipe.description ?? `Recipe ${recipe.id}`}</h3>
                        {recipe.category && <div className={styles.category}>{recipe.category}</div>}
                    </div>
                </div>

                {recipe.description && <p className={styles.description}>{recipe.description}</p>}

                {visible.length > 0 && (
                    <div className={styles.keywords}>
                        {visible.map((k, i) => (
                            <span key={i} className={`${styles.chip} ${styles[palette[i % palette.length]]}`}>{k}</span>
                        ))}
                    </div>
                )}

                <hr className={styles.divider} />

                <div className={styles.summary}>
                    <div className={styles.summaryItem}>
                        <FontAwesomeIcon icon={faList} className={styles.icon} />
                        <div className={styles.summaryText}>{nIngredients ?? '—'} ingredients</div>
                    </div>

                    <div className={styles.summaryItem}>
                        <FontAwesomeIcon icon={faClock} className={styles.icon} />
                        <div className={styles.summaryText}>{recipe.total_time_minutes ?? '—'} min</div>
                    </div>

                    <div className={styles.summaryItem}>
                        <FontAwesomeIcon icon={faFire} className={styles.icon} />
                        <div className={styles.summaryText}>{displayCalories ?? '—'} kcal</div>
                    </div>

                    <div className={styles.summaryItem}>
                        <FontAwesomeIcon icon={faStar} className={styles.icon} />
                        <div className={styles.summaryText}>{recipe.aggregated_rating ?? recipe.score ?? '—'}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
