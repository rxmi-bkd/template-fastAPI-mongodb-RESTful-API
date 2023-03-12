from fastapi import FastAPI
from app.core.config import CONFIG
from app.api.api_v1.api import api_router
from app.db.init_db import init_mongo_client, init_mongo_db

app = FastAPI(title=CONFIG.title,
              description=CONFIG.description,
              version=CONFIG.version,
              openapi_url=f'{CONFIG.base_url}/openapi.json',
              docs_url=f'{CONFIG.base_url}/docs',
              redoc_url=f'{CONFIG.base_url}/redocs',
              contact={"name": f'{CONFIG.contact_name}',
                       "url": f"{CONFIG.contact_url}",
                       "email": f"{CONFIG.contact_email}"})


@app.on_event("startup")
def startup_client():
    client = init_mongo_client(CONFIG.atlas_url)
    database = init_mongo_db(client=client,
                             database_name=CONFIG.db_name)

    app.mongodb_client = client
    app.database = database


@app.on_event("shutdown")
def shutdown_client():
    app.mongodb_client.close()


app.include_router(router=api_router,
                   prefix=CONFIG.base_url)
