from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.graphql_manager.service import graphql_app
from src.user.service import user_router, guest_router
from src.auth.service import auth_router
from src.shared_preference.service import preference_router


origins = [
    "http://localhost:8001",
]


main_app = FastAPI(title="Deepmode")

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
main_app.include_router(guest_router, prefix="/api/user", tags=["User"])
main_app.include_router(user_router, prefix="/api/user", tags=["User"])
main_app.include_router(
    preference_router, prefix="/api/shared-preference", tags=["Shared Preference"]
)

main_app.include_router(
    graphql_app, prefix="/api/graphql", tags=["Word", "Spaced Repetition"]
)


@main_app.get("/", tags=["Admin"])
async def main():
    return {"api", "hello world"}
