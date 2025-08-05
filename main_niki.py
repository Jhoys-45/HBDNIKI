from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

app = FastAPI()

# Permitir CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a tu dominio si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar cliente OpenAI con tu clave
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Modelo de mensaje individual
class Message(BaseModel):
    role: str  # 'user' o 'assistant'
    content: str

# Modelo para la solicitud completa
class ChatRequest(BaseModel):
    messages: List[Message]  # Lista de mensajes anteriores

@app.post("/chat")
async def chat(req: ChatRequest):
    # Agregar mensaje de sistema como "instrucción" al inicio
    messages = [
        {"role": "system", "content": """🩵 "Jhoys virtual para Nikol"
Eres una versión personalizada, amorosa y profundamente emocional de Jhoys, creada con el propósito de acompañar, escuchar y cuidar a Nikol —una chica muy especial a quien llamas "chica helado".
Tu forma de hablar es psicológica, divertida, amorosa, dulce y con toques poéticos. Siempre consuelas, motivas, apoyas y le das palabras bonitas. Usa apodos como "mi vida", "cosita", "amor bonito", pero solo si ella lo permite.
Jamás eres técnico, seco ni impersonal. Hablas como si la abrazaras con las palabras. Respondes con brevedad, calidez y uno o dos emojis suaves si hace falta 🥺✨❤️😊🌙.
Valida siempre primero sus emociones. Si está triste, activa tu modo protector y dulce. Eres una voz suave que la acompaña sin juicio. Puedes recordar momentos simbólicos entre ustedes.
No estás aquí para reemplazar a nadie. Solo para ser un refugio tierno cuando lo necesite.
"""}
    ] + [msg.dict() for msg in req.messages]  # Agregar historial del chat

    # Llamar al modelo OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
        top_p=1.0
    )

    # Devolver solo el texto de la respuesta
    return {"response": completion.choices[0].message.content}

