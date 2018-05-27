import graphene
from app.users.schemas import UserType
from .controllers import sign_up, sign_in


class SignInInput(graphene.InputObjectType):
    contact = graphene.String(required=True)
    password = graphene.String(required=True)


class SignUpInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class SignInMutation(graphene.Mutation):
    class Arguments:
        payload = SignInInput(required=True)

    token = graphene.String(required=True)
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, payload=None):
        token, user = sign_in(payload)
        return SignUpMutation(token=token, user=user)


class SignUpMutation(graphene.Mutation):
    class Arguments:
        payload = SignUpInput(required=True)

    token = graphene.String(required=True)
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, payload=None):
        token, user = sign_up(payload)
        return SignUpMutation(token=token, user=user)


class AuthMutation(graphene.ObjectType):
    sign_in = SignInMutation.Field()
    sign_up = SignUpMutation.Field()
