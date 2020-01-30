from ariadne import ObjectType, QueryType, snake_case_fallback_resolvers
from ariadne_extensions.federation import FederatedManager, FederatedObjectType

from schema.data_interface import DataStorage

"""
Creates the Schema and adds the Federation Declerations to it according to the [https://www.apollographql.com/docs/apollo-server/federation/federation-spec/](Apollo Spec).
"""
class SchemaCreator:

    def __init__(self):
        self.ds = DataStorage()

    def getSchema(self):

        query = QueryType()

        manager = FederatedManager(
            schema_sdl_file='schema/schema.graphql',
            query=query,
        )

        @query.field("users")
        def resolve_users(*_, **kwargs):
            return self.ds.getUser(**kwargs)

        user = ObjectType("User")

        manager.add_types(user)
        manager.add_types(snake_case_fallback_resolvers)

        return manager.get_schema()