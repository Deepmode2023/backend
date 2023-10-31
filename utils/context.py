from strawberry.fastapi import BaseContext


class AuthContext(BaseContext):
    @property
    def get_raw_token(self):
        authorization = self.request.headers.get("Authorization", "None")
        return authorization


async def get_context() -> AuthContext:
    return AuthContext()
