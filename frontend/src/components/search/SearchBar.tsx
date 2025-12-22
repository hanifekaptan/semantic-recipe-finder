import React from 'react'
import styles from './SearchBar.module.css'
import Spinner from '../../components/common/Spinner'

type Props = {
    value?: string
    onChange?: (v: string) => void
    onSearch?: (q?: string) => void
    placeholder?: string
    loading?: boolean
    className?: string
}

export default function SearchBar({ value = '', onChange, onSearch, placeholder = 'Search...', loading = false, className }: Props) {
    const [q, setQ] = React.useState<string>(value)

    React.useEffect(() => setQ(value), [value])

    const submit = (e?: React.FormEvent) => {
        e?.preventDefault()
        onChange?.(q)
        onSearch?.(q)
    }

    return (
        <form onSubmit={submit} className={`${styles.root} ${className ?? ''}`.trim()}>
            <div className={styles.inputWrap}>
                <input
                    className={styles.input}
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    onBlur={() => onChange?.(q)}
                    placeholder={placeholder}
                    aria-label="search"
                />
                <button type="submit" className={styles.searchButton} aria-label="search">
                    {loading ? <Spinner /> : <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" /><circle cx="11" cy="11" r="6" stroke="currentColor" strokeWidth="1.6" /></svg>}
                </button>
            </div>
        </form>
    )
}
