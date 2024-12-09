import strawberry
from strawberry.fastapi import GraphQLRouter

from src.words.service import Mutation as MutationWords
from src.words.service import Query as QueryWords
from utils.context.auth import get_context


@strawberry.type
class Mutation(MutationWords):
    pass


@strawberry.type
class Query(QueryWords):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
