from fastapi import FastAPI, status
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.shared_preference.service import preference_router
from src.auth.service import auth_router
from src.user.service import user_router, guest_router
from src.graphql_manager.service import graphql_app

from utils.security import JWTAuth


main_app = FastAPI(title="Deepmode")


main_app.add_middleware(AuthenticationMiddleware, backend=JWTAuth(),)
main_app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
main_app.include_router(guest_router, prefix="/api/user", tags=["User"])
main_app.include_router(user_router, prefix="/api/user", tags=["User"])
main_app.include_router(
    preference_router, prefix="/api/shared-preference", tags=["Shared Preference"])

main_app.include_router(graphql_app, prefix="/api/graphql", tags=['Word'])


@main_app.get("/", tags=["Admin"])
async def main():
    return {"message": "Hello Worlsdfsdd"}
