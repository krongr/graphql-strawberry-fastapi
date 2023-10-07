"""
main.py

This module initializes a FastAPI application with a MongoDB backend
and sets up routing for GraphQL operations. It provides a health check
endpoint to verify that the service is operational.

Usage:
    Run the script directly to start the FastAPI server:
    $ python main.py

    Or run uvicorn from terminal:
    $ uvicorn main:app --host 0.0.0.0 --port 80
"""


import mongoengine
from fastapi import FastAPI

from gql.schema import gql_router
from settings import MONGODB_CONNECTION


# Initializing MongoDB connection for the app.
mongoengine.connect(**MONGODB_CONNECTION)

app = FastAPI()

@app.get('/')
def health_check():
    """
    Check the health status of the service.
    """
    return {'status': 'ok'}

# Including the GraphQL router to the FastAPI app.
app.include_router(gql_router, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True)
