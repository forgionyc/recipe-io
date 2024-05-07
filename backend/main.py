import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from werkzeug.utils import secure_filename

from identify import model_predict
from recipe_bot import Chatbot, Vectorstore

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = FastAPI()
vectorstore = Vectorstore()
chatbot = Chatbot(vectorstore)

# Set origins
DEV_FRONT_URL = os.getenv("DEV_FRONT_URL")
PROD_FRONT_URL = os.getenv("PROD_FRONT_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

origins = [
    DEV_FRONT_URL,
    PROD_FRONT_URL,
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Reemplaza esto con el origen de tu aplicación Angular
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],  # Método HTTP permitido en las solicitudes CORS
    allow_headers=["Authorization", "Content-Type"],
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Prediction(BaseModel):
    filename: str
    prediction: tuple


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(
        Date, default=datetime.now().date()
    )  # Se establece automáticamente la fecha
    description = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="recipes")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)

    recipes = relationship("Recipe", back_populates="user")


Base.metadata.create_all(bind=engine)


class RecipeCreate(BaseModel):
    name: str
    description: str
    content: str
    username: str


class UserCreate(BaseModel):
    username: str


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
async def welcome():
    return {"message": "Bienvenido a mi API de recetas"}


@app.post("/api/classification")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    filename = secure_filename(file.filename)
    target_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(target_path, "wb") as buffer:
        buffer.write(await file.read())
    print(target_path)

    # Replace model_predict with your actual prediction function
    prediction = model_predict(target_path)
    print(prediction)

    return prediction


@app.post("/api/chat")
async def chat_endpoint(message: str):
    # Process the incoming message with the chatbot
    response_text = chatbot.process_message(message)

    if response_text is None:
        raise HTTPException(status_code=500, detail="Chatbot error")

    return {"response": response_text}


@app.post("/api/recipes/")
async def create_recipe(recipe: RecipeCreate):
    db = SessionLocal()
    # Buscar el usuario por su nombre de usuario
    user = db.query(User).filter(User.username == recipe.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Crear la receta asociada al usuario
    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        content=recipe.content,
        user_id=user.id,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@app.get("/api/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return recipe


@app.get("/api/users/{username}/recipes/")
async def get_user_recipes(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()
    if not recipes:
        raise HTTPException(
            status_code=404, detail="No se encontraron recetas para este usuario"
        )
    return recipes


@app.post("/api/users/")
async def create_user(user: UserCreate):
    db = SessionLocal()

    # Verificar si el nombre de usuario ya existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        # Si el nombre de usuario ya existe, puedes optar por simplemente continuar
        # o puedes devolver un mensaje informativo
        return existing_user

    # Si el nombre de usuario no existe, crear el nuevo usuario
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
