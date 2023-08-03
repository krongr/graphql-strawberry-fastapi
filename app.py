from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from schema import schema


app = FastAPI()

@app.get('/')
def health():
    return {'status': 'ok'}

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
