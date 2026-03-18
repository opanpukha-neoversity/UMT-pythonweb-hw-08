from fastapi import FastAPI

from src.api.contacts import router as contacts_router
from src.database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contacts API",
    description="REST API for storing and managing contacts",
    version="1.0.0",
)

app.include_router(contacts_router)


@app.get("/", tags=["healthcheck"])
def read_root():
    return {"message": "Contacts API is running"}
