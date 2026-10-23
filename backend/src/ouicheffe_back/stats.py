"""
1ère requête: récupérer les ingrédients non utilisés dans aucune recette

SELECT i.id, i.name
FROM ingredients i
LEFT JOIN recipe_ingredients ri ON ri.ingredient_id = i.id
WHERE ri.ingredient_id IS NULL;

2ème requete :
SELECT i.id, i.name, COUNT(*) AS nb_recettes
FROM ingredients i
JOIN recipe_ingredients ri ON ri.ingredient_id = i.id
GROUP BY i.id
ORDER BY nb_recettes DESC;
"""
from sqlalchemy import select
from .database import SessionLocal
from .models import Ingredient, RecipeIngredient

# 1. récupérer les ingrédients non utilisés dans aucune recette
def unused_ingredients(db):
    # statement
    stmt = (
        select(Ingredient.id, Ingredient.name)
        .outerjoin(RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id)
        .where(RecipeIngredient.ingredient_id.is_(None))
    )
    print(stmt) 
    return db.execute(stmt)

    

if __name__ == "__main__":
    db = SessionLocal()
    try:
        for row in unused_ingredients(db):
            print(row.id, row.name)
    finally:
        db.close()