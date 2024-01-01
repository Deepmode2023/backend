import strawberry
from strawberry.fastapi import GraphQLRouter
from src.words.service import Query as QueryWords, Mutation as MutationWords
from src.spaced_repetitions.service import Query as QuerySpacedRepetiotions, Mutation as MutationSpacedRepetitions
from utils.context.auth import get_context


@strawberry.type
class Mutation(MutationWords, MutationSpacedRepetitions):
    pass


@strawberry.type
class Query(QueryWords, QuerySpacedRepetiotions):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
