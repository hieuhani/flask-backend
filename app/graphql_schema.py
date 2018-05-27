import graphene
from .users.schemas import UserQuery
from .auth.schemas import AuthMutation


class Query(graphene.ObjectType):
    user = graphene.Field(UserQuery)


class Mutation(graphene.ObjectType):
    user = graphene.Field(AuthMutation)

    def resolve_user(self, info):
        return AuthMutation()


schema = graphene.Schema(query=Query, mutation=Mutation)
