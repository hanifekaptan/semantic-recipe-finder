import type { FrontendRecipeDetail } from '../../types/index.types'
import Modal from '../common/Modal'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faList, faFire } from '@fortawesome/free-solid-svg-icons'
import { faClock, faStar } from '@fortawesome/free-regular-svg-icons'

type Props = {
    recipe?: FrontendRecipeDetail | null
    open: boolean
    onClose: () => void
}

function NutrientPie({ label, percent, value, color }: { label: string; percent?: number | null; value?: string | null; color?: string }) {
    const p = typeof percent === 'number' ? percent : (percent ? Number(percent) : NaN)
    const pct = Number.isFinite(p) ? Math.max(0, Math.min(100, p)) : NaN
    const radius = 20
    const stroke = 8
    const circumference = 2 * Math.PI * radius
    const filled = Number.isFinite(pct) ? (circumference * (pct / 100)) : 0
    const empty = circumference - filled

    return (
        <div className="nutrient-pie" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 110 }}>
            <svg width={72} height={72} viewBox="0 0 72 72" role="img" aria-label={`${label} ${Number.isFinite(pct) ? pct.toFixed(1) + '%' : 'no data'}`}>
                <circle cx="36" cy="36" r={radius} fill="none" stroke="#f3f4f6" strokeWidth={stroke} />
                {Number.isFinite(pct) && (
                    <circle cx="36" cy="36" r={radius} fill="none" stroke={color ?? '#6ca86b'} strokeWidth={stroke} strokeLinecap="round" strokeDasharray={`${filled} ${empty}`} transform="rotate(-90 36 36)" />
                )}
                <text x="36" y="41" textAnchor="middle" fontSize="12" fill="#0f172a">{Number.isFinite(pct) ? `${pct.toFixed(0)}%` : '—'}</text>
            </svg>
            <div style={{ marginTop: 6, fontSize: 13, fontWeight: 600 }}>{label}</div>
            <div style={{ fontSize: 12, color: '#6b7280' }}>{value ?? ''}</div>
        </div>
    )
}

export default function RecipeDetailModal({ recipe, open, onClose }: Props) {
    return (
        <Modal open={open} onClose={onClose}>
            <div style={{ width: 750, maxWidth: 'calc(100vw - 48px)', height: '80vh', maxHeight: 'calc(100vh - 48px)', overflow: 'auto', padding: 20 }}>
                {!recipe ? (
                    <div style={{ padding: 40, textAlign: 'center' }}>Loading...</div>
                ) : (
                    <div>
                        <header style={{ marginBottom: 8 }}>
                            <h2 style={{ margin: 0, fontSize: 22, lineHeight: 1.1 }}>{recipe.title ?? `Recipe ${recipe.id}`}</h2>
                            {recipe.category && <div style={{ color: '#6b7280', fontSize: 13 }}>{recipe.category}</div>}
                        </header>

                        {recipe.description && <p style={{ color: '#6b7280', marginTop: 8 }}>{recipe.description}</p>}

                        {recipe.keywords && recipe.keywords.length > 0 && (
                            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 8 }}>
                                {recipe.keywords.map((k, i) => (
                                    <span key={i} style={{ background: '#f3f4f6', padding: '6px 10px', borderRadius: 999, fontSize: 13 }}>{k}</span>
                                ))}
                            </div>
                        )}

                        <hr style={{ border: 'none', height: 1, background: 'rgba(15,23,42,0.06)', margin: '18px 0' }} />

                        <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <FontAwesomeIcon icon={faList} style={{ color: '#a1a1a1' }} />
                                <div style={{ fontWeight: 600 }}>{String(recipe.n_ingredients ?? '—')}</div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <FontAwesomeIcon icon={faClock} style={{ color: '#a1a1a1' }} />
                                <div style={{ fontWeight: 600 }}>{String(recipe.total_time_minutes ?? '—')} min</div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <FontAwesomeIcon icon={faFire} style={{ color: '#a1a1a1' }} />
                                <div style={{ fontWeight: 600 }}>{String(recipe.calories ?? '—')} kcal</div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <FontAwesomeIcon icon={faStar} style={{ color: '#a1a1a1' }} />
                                <div style={{ fontWeight: 600 }}>{String(recipe.aggregated_rating ?? recipe.score ?? '—')}</div>
                            </div>
                        </div>

                        <hr style={{ border: 'none', height: 1, background: 'rgba(15,23,42,0.06)', margin: '12px 0' }} />

                        <section style={{ marginTop: 8 }}>
                            <h4 style={{ margin: '8px 0', fontSize: 14, letterSpacing: 0.6 }}>INGREDIENTS</h4>
                            {Array.isArray(recipe.ingredients) && recipe.ingredients.length > 0 ? (
                                <ol className="ingredients-list">
                                    {recipe.ingredients.map((it, i) => (
                                        <li key={i} className="ingredient-item">{it}</li>
                                    ))}
                                </ol>
                            ) : (
                                <div style={{ color: '#6b7280' }}>No ingredient information available.</div>
                            )}
                        </section>

                        <hr style={{ border: 'none', height: 1, background: 'rgba(15,23,42,0.06)', margin: '12px 0' }} />

                        <section style={{ marginTop: 8 }}>
                            <h4 style={{ margin: '8px 0', fontSize: 14, letterSpacing: 0.6 }}>INSTRUCTIONS</h4>
                            {recipe.instructions ? (
                                <div className="instructions-list">
                                    {recipe.instructions.split(/\r?\n|\.\s+/).map((s) => s.trim()).filter(Boolean).map((step, i) => (
                                        <div key={i} className="instruction-item" style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
                                            <input className="instruction-checkbox" type="checkbox" tabIndex={-1} />
                                            <div style={{ flex: 1 }}>{step}</div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div style={{ color: '#6b7280' }}>No instructions available.</div>
                            )}
                        </section>

                        <hr style={{ border: 'none', height: 1, background: 'rgba(15,23,42,0.06)', margin: '12px 0' }} />

                        <section style={{ marginTop: 8 }}>
                            <h4 style={{ margin: '8px 0', fontSize: 14, letterSpacing: 0.6 }}>NUTRITION (%)</h4>
                            <div className="nutrition-row" style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                                <NutrientPie label="Fat" percent={recipe.nutrition_percents?.fat ?? null} value={recipe.nutrition_content?.fat ?? undefined} color="#f97316" />
                                <NutrientPie label="Protein" percent={recipe.nutrition_percents?.protein ?? null} value={recipe.nutrition_content?.protein ?? undefined} color="#16a34a" />
                                <NutrientPie label="Sugar" percent={recipe.nutrition_percents?.sugar ?? null} value={recipe.nutrition_content?.sugar ?? undefined} color="#7c3aed" />
                                <NutrientPie label="Carbohydrate" percent={recipe.nutrition_percents?.carbohydrate ?? null} value={recipe.nutrition_content?.carbohydrate ?? undefined} color="#0284c7" />
                            </div>
                        </section>
                    </div>
                )}
            </div>
        </Modal>
    )
}
