from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this later to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables
# Base.metadata.create_all(bind=engine)

# register_routes(app)