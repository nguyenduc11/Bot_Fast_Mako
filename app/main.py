from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import RedirectResponse

from app.routers import home, about, auth, todos, flashcards

app = FastAPI()

# MongoDB Atlas connection URI
mongodb_uri = "mongodb+srv://nguyenduc11:NJtdKiz5DQDU4HE2@clusterflaskweb.refwjuv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFlaskWeb"

# MongoDB connection


@app.on_event("startup")
async def startup_db_client():
    try:
        app.mongodb_client = AsyncIOMotorClient(mongodb_uri)
        # Explicitly connecting to 'flask_web' database
        app.mongodb = app.mongodb_client.flask_web
        app.mongodb.flashcard = app.mongodb_client.flashcard
        print("Connected to MongoDB Atlas - flask_web database")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        # You might want to handle this error more gracefully in a production environment


@app.on_event("shutdown")
async def shutdown_db_client():
    if hasattr(app, 'mongodb_client'):
        app.mongodb_client.close()
        print("Closed MongoDB Atlas connection")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Mako templates
templates = TemplateLookup(directories=["app/templates"])

# Include routers with prefixes
app.include_router(home.router, prefix="/home")
app.include_router(about.router, prefix="/about")
app.include_router(auth.router, prefix="/auth")
app.include_router(todos.router, prefix="/todos")
app.include_router(flashcards.router, prefix="/flashcards")

# Make templates available for all routes


@app.middleware("http")
async def add_templates_to_request(request, call_next):
    request.state.templates = templates
    response = await call_next(request)
    return response

# Root redirect


@app.get("/")
async def root():
    return RedirectResponse(url="/home")
