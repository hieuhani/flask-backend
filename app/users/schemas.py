import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User, Contact


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
        exclude_fields = ('password_hash',)


class ContactType(SQLAlchemyObjectType):
    class Meta:
        model = Contact
        interfaces = (relay.Node,)


class UserQuery(graphene.ObjectType):
    profile = graphene.String()
