from fastapi import FastAPI
from modules.auth.handlers import auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from modules.user.handlers import user_router, guest_router
from utils.security import JWTAuth
from modules.graphql_manager.handlers import graphql_app


main_app = FastAPI(title="Deepmode")

main_app.add_middleware(AuthenticationMiddleware, backend=JWTAuth(),)
main_app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
main_app.include_router(guest_router, prefix="/api/user", tags=["user"])
main_app.include_router(user_router, prefix="/api/user", tags=["user"])

main_app.include_router(graphql_app, prefix="/api/graphql",
                        tags=['word, shared prefrence'])


@main_app.get("/", tags=["main"])
async def main():
    return {"message": "Hello Worlsdfsdd"}
