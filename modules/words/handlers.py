import strawberry
from strawberry.types import Info

from utils.params_helpers import CommonParams
from utils.security import JWTAuth


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_flavour(self, name: str, info: Info) -> bool:
        return True


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[JWTAuth])
    def get_words(self, common_params: CommonParams = {}, ) -> str:
        return f"Hello"
