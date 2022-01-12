from fastapi import FastAPI
from graphene import ObjectType, List, String, Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from schema.courses import courseSchema
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_route("/", GraphQLApp(schema=courseSchema, on_get=make_graphiql_handler()))
