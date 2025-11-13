from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database import Base, engine
from src.routes import article_routes, user_routes, comment_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Blog Platform")
bearer_scheme = HTTPBearer()

app.include_router(user_routes.router)
app.include_router(article_routes.router)
app.include_router(comment_routes.router)
