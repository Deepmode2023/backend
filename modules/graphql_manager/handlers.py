from fastapi import Depends

import strawberry
from strawberry.types import Info
from strawberry.fastapi import GraphQLRouter
from modules.words.handlers import Query as Query_words
from utils.context import get_context


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_flavour(self, name: str, info: Info) -> bool:

        return True


@strawberry.type
class Query(Query_words):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context,)
