from pymongo import MongoClient
from pymongo.database import Database


def init_mongo_client(atlas_url: str) -> MongoClient:
    try:
        client = MongoClient(atlas_url)
        # Check if the connection is successful
        client.server_info()

        return client

    except Exception as e:
        raise ConnectionError("Could not connect to MongoDB client")


def init_mongo_db(client: MongoClient, database_name: str) -> Database:
    try:
        # Check if the database exists
        db = client[database_name]

        return db

    except Exception as e:
        raise ConnectionError("Could not connect to MongoDB database")
