from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    creator = "creator"

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[UserRole]
    name: Mapped[str]
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))

class Brigade(Base):
    __tablename__ = "brigades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    unit: Mapped[str]
    ingredient_category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"))
    is_regular: Mapped[bool]

class CustomizedItems(Base):
    __tablename__ = "customized_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    note: Mapped[Optional[str]]
    is_checked: Mapped[bool]
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    prep_time: Mapped[int]
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    servings: Mapped[int]
    image_url: Mapped[Optional[str]]
    tag: Mapped["Tag"] = relationship()

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    quantity: Mapped[float]

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_checked: Mapped[bool]
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

class SelectedRecipe(Base):
    __tablename__ = "selected_recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))
    selected_servings: Mapped[int]

class Instruction(Base):
    __tablename__ = "instructions"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    step: Mapped[int]
    instruction: Mapped[str]