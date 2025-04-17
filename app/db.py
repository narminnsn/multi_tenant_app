from tortoise import Tortoise
from app.config.settings import settings
from fastapi import HTTPException

TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["app.core.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    try:
        # Initialize core database connection
        await Tortoise.init(
            db_url=settings.DATABASE_URL, modules={"models": ["app.core.models"]}
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error initializing core database: {str(e)}"
        )


# async def init_tenant_db(tenant_id: str):
#     try:
#         tenant_db_url = f"postgresql://user:password@localhost/{tenant_id}_db"
#         # Initialize tenant-specific database connection
#         await Tortoise.init(
#             db_url=tenant_db_url,
#             modules={"models": ["app.tenants.models"]}
#         )
#         await Tortoise.generate_schemas()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error initializing tenant database: {str(e)}")
