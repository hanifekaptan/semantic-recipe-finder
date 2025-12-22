export default function Spinner() {
    return (
        <div style={{ display: 'inline-block' }} aria-label="loading">
            <svg width="24" height="24" viewBox="0 0 50 50">
                <circle cx="25" cy="25" r="20" strokeWidth="5" stroke="rgba(0,0,0,0.15)" fill="none" />
                <path d="M45 25a20 20 0 0 0-20-20" strokeWidth="5" stroke="var(--color-primary)" fill="none" strokeLinecap="round" />
            </svg>
        </div>
    );
}
