# Semantic Recipe Finder — Frontend


Project Overview
----------------
Semantic Recipe Finder is a small frontend that lets users search for recipes using semantic text queries, browse results, and open a detail modal with ingredients, instructions and nutrition info. It is designed as a lightweight UI shell that talks to a separate backend API.

Features
--------
- Free-text semantic search with paginated results
- Single-column responsive recipe cards
- Recipe detail modal with ingredients, instructions, and nutrient visualization
- Lightweight client-side caching for recipe details
- Accessible keyboard focus outlines and responsive layout

Tech Stack
----------
- React (function components + hooks)
- TypeScript
- Vite (dev server + build)
- Styling: global CSS + CSS modules
- Icons: Font Awesome (CDN)

Quick Start
-----------
Install dependencies and run the dev server:

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
```

Project Structure
-----------------
High-level layout of the important files and folders:

- `src/`
	- `components/` — reusable UI components (cards, modal, buttons)
	- `pages/` — page entry points such as `HomePage`
	- `api/recipeService.ts` — backend API helpers and mappers
	- `hooks/` — custom hooks (e.g. `useRecipes`)
	- `types/` — TypeScript types and mapping helpers
	- `assets/styles/` — global styles and CSS variables

Components Overview
-------------------
- `SearchBar` — input and submit control that updates the query and triggers searches.
- `RecipeCard` — presents brief recipe info in the results list; opens the detail modal.
- `RecipeList` — layout wrapper rendering `RecipeCard` instances in a single column.
- `RecipeDetailModal` — centered modal showing full recipe detail: ingredients, plain checkbox instructions, nutrition pies, and metadata.
- `Modal` (common) — backdrop + content wrapper that handles dismiss and basic accessibility.
- `useRecipes` (hook) — manages query state, loading, error and calls `searchRecipes` from `recipeService`.

Notes & Next Steps
------------------
- The app currently uses a CDN for Font Awesome for quick setup; if you prefer component usage, install official Font Awesome packages and update imports.
