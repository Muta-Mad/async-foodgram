from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.recipes.models import Recipe
from api.users.schemas import RecipeSubscribers, SubscribeSchemas


async def get_recipe_subscribers(
        session: AsyncSession, 
        author_id: int,
        limit: int | None
    ):
    query = select(Recipe).where(Recipe.author_id == author_id)
    if limit:
        query = query.limit(limit)
    result = await session.execute(query)
    recipes = result.scalars().all()
    return [
        RecipeSubscribers(
            id=recipe.id,
            name=recipe.name,
            image=recipe.image,
            cooking_time=recipe.cooking_time
        )
        for recipe in recipes
    ]

async def get_subscribe_schema(author, session, recipes_limit=None):
    recipes = await get_recipe_subscribers(session, author.id, recipes_limit)
    return SubscribeSchemas(
        id=author.id,
        email=author.email,
        username=author.username,
        first_name=author.first_name,
        last_name=author.last_name,
        avatar=author.avatar,
        is_subscribed=True,
        recipes=recipes,
        recipes_count=len(recipes)
    )
