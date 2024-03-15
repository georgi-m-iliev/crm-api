from fastapi import FastAPI

from app.routers import items, users

app = FastAPI()


app.include_router(users.users)


@app.get("/")
async def root():
    return {"message": "Hello!!"}
