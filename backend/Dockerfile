#stage builder 
#on copie l'image python pour "atelier temporaire" pour installer les dépendances
FROM python:3.12-slim AS builder

#on copie l'image officielle de uv pour l'atelier
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

#on définit le dossier de travail dans le container
WORKDIR /app

#on copie les dépénces à installer et respecter dans ma liste de dépendances
COPY pyproject.toml uv.lock ./

#installer les dépendances dans un environnement virtuel
RUN uv sync --frozen --no-dev --no-install-project

#on copie le code source du projet dans le container
COPY src ./src
#on installe le code source par dessus les dépendence
#maintenant on finit l'atelier et on a le résultat final dans le dossier .venv
RUN uv sync --frozen --no-dev


FROM python:3.12-slim

WORKDIR /app
#on copie seulement le résultat final de l'atelier dans le container final
COPY --from=builder /app/.venv /app/.venv

COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "ouicheffe_back.main:app", "--host=0.0.0.0", "--port=8000"]
