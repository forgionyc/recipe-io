import os

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],  # Reemplaza esto con el origen de tu aplicación Angular
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],  # Método HTTP permitido en las solicitudes CORS
    allow_headers=["Authorization", "Content-Type"],
)


class Prediction(BaseModel):
    filename: str
    prediction: tuple


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def read_root():
    return {"Hello": "World"}


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
