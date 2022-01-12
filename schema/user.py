from graphene import String, ObjectType


class User(ObjectType):
    id = graphene.ID()
    name = graphene.String()
