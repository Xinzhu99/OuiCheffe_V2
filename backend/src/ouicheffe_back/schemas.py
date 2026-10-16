from pydantic import BaseModel
from typing import Optional

class TagOut(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True,
    }
class RecipeOut(BaseModel):
    id: int
    name: str
    prep_time: int
    servings: int
    image_url: Optional[str] = None
    tag: TagOut    
    model_config = {
        "from_attributes": True,
    }