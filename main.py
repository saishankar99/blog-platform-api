from fastapi import FastAPI
from routers import users,posts
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Blog Platform API")
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/health")
def health():
    return {"status": "ok"}