import strawberry
from strawberry.fastapi import GraphQLRouter


from modules.words.handlers import Query as Query_words, Mutation as Mutation_words
from utils.context import get_context


@strawberry.type
class Mutation(Mutation_words):
    pass


@strawberry.type
class Query(Query_words):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context,)
