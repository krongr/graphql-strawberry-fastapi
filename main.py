from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from gql.shema import schema


app = FastAPI()

@app.get('/')
def health_check():
    return {'status': 'ok'}

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True)
