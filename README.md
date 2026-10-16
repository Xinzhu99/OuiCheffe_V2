# OuiCheffe!

Application web de recettes de cuisine : consultation de recettes, sélection de plats et génération de listes de courses.

🔗 **Site en ligne : http://oui-cheffe.xinzhu.fr/**

## 🧰 Stack technique

| Partie | Technologie |
| --- | --- |
| Frontend | Vue.js (Vite) + Tailwind CSS |
| Backend | FastAPI (Python) |
| Base de données | PostgreSQL |
| ORM | SQLAlchemy |
| Authentification | FastAPI Users |
| Gestion des dépendances | npm (front) · uv (back) |

## Prérequis

- Docker et Docker Compose
- Node.js `^22.18.0` ou `>=24.12.0`
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (seulement pour les données de test)

## Installation

```bash
git clone git@github.com:Xinzhu99/OuiCheffe_V2.git
cd OuiCheffe_V2
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Lancement

```bash
# 1. Base de données + API
docker compose up -d --build
docker compose exec back alembic upgrade head

# 2. Frontend
cd frontend
npm install
npm run dev
```

- Frontend : http://localhost:5173
- API : http://localhost:8000 (documentation sur `/docs`)

### Données de test (optionnel)

Depuis la racine du projet :

```bash
cd backend
uv sync
DATABASE_URL='postgresql://ouicheffe:ouicheffe@localhost:5432/ouicheffe' uv run python -m ouicheffe_back.seed
```
