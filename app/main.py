from fastapi import FastAPI
from app.api.v1 import auth, tenant, organizations
from app.db import init_db
from tortoise import Tortoise

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tenant.router, prefix="/api", tags=["tenants"])
app.include_router(organizations.router, prefix="/api", tags=["organizations"])


@app.get("/")
async def root():
    return {"message": "Welcome to the multi-tenant app!"}


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()
