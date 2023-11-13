from fastapi import FastAPI, Depends
from src.auth.service import auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from src.user.service import user_router, guest_router
from utils.security import JWTAuth
from src.graphql_manager.service import graphql_app


main_app = FastAPI(title="Deepmode")

main_app.add_middleware(AuthenticationMiddleware, backend=JWTAuth(),)
main_app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
main_app.include_router(guest_router, prefix="/api/user", tags=["user"])
main_app.include_router(user_router, prefix="/api/user", tags=["user"])

main_app.include_router(graphql_app, prefix="/api/graphql",
                        tags=['word'])


@main_app.get("/", tags=["main"])
async def main():
    return {"message": "Hello Worlsdfsdd"}
