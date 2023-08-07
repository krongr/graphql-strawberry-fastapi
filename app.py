from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from resolvers import schema


app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)