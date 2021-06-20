from graphene import ObjectType, String


class Query(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "world!"


class RootQuery(Query, ObjectType):
    pass
