"""
Script de génération de données fictives pour développement local.
Usage : uv run python -m ouicheffe_back.seed  
"""
from faker import Faker
from .database import SessionLocal
from .models import Tag, IngredientCategory, Ingredient, Recipe, RecipeIngredient, Instruction

fake = Faker("fr_FR")

def seed():
    db = SessionLocal()

    # --- 1. Tags (sans dépendance) ---
    tag_names = ["Entrée", "Plat", "Dessert", "Végétarien", "Rapide"]
    tags = [Tag(name=name) for name in tag_names]
    db.add_all(tags)
    db.flush()  # envoie les INSERT sans encore committer, pour récupérer les .id générés

    # --- 2. Catégories d'ingrédients (sans dépendance) ---
    category_names = ["Légumes", "Viandes", "Épicerie", "Produits laitiers", "Épices"]
    categories = [IngredientCategory(name=name) for name in category_names]
    db.add_all(categories)
    db.flush()

    # --- 3. Ingrédients (dépend des catégories) ---
    units = ["g", "kg", "ml", "l", "unité", "cuillère à soupe"]
    ingredients = []
    for _ in range(25):
        ingredients.append(Ingredient(
            name=fake.word().capitalize(),
            unit=fake.random_element(units),
            ingredient_category_id=fake.random_element(categories).id,
            is_regular=fake.boolean(chance_of_getting_true=30),
        ))
    db.add_all(ingredients)
    db.flush()

    # --- 4. Recettes (dépend des tags) ---
    recipes = []
    for _ in range(10):
        recipes.append(Recipe(
            name=fake.sentence(nb_words=3).rstrip("."),
            prep_time=fake.random_int(min=10, max=90),
            tag_id=fake.random_element(tags).id,
            servings=fake.random_int(min=1, max=8),
            image_url=None,
        ))
    db.add_all(recipes)
    db.flush()

    # --- 5. Liaison recettes <-> ingrédients (dépend des deux) ---
    recipe_ingredients = []
    for recipe in recipes:
        # chaque recette reçoit entre 3 et 7 ingrédients pris au hasard
        chosen = fake.random_elements(elements=ingredients, length=fake.random_int(3, 7), unique=True)
        for ingredient in chosen:
            recipe_ingredients.append(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=round(fake.random.uniform(0.5, 500), 1),
            ))
    db.add_all(recipe_ingredients)

    # --- 6. Instructions (dépend des recettes) ---
    instructions = []
    for recipe in recipes:
        nb_steps = fake.random_int(min=3, max=6)
        for step_num in range(1, nb_steps + 1):
            instructions.append(Instruction(
                recipe_id=recipe.id,
                step=step_num,
                instruction=fake.sentence(nb_words=12),
            ))
    db.add_all(instructions)

    db.commit()
    db.close()
    print(f"{len(tags)} tags, {len(categories)} catégories, {len(ingredients)} ingrédients, "
          f"{len(recipes)} recettes, {len(recipe_ingredients)} liaisons, {len(instructions)} instructions créés.")

if __name__ == "__main__":
    seed()