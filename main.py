import mongoengine
from fastapi import FastAPI

from gql.schema import gql_router
from settings import MONGODB_CONNECTION


mongoengine.connect(**MONGODB_CONNECTION)

app = FastAPI()

@app.get('/')
def health_check():
    return {'status': 'ok'}

app.include_router(gql_router, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True)
