from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/upload")
async def upload_knowledge(text: str = Form(...)):
    with open("knowledge_base.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return {"message": "Knowledge uploaded successfully."}

@app.post("/chat")
async def chat_endpoint(message: dict):
    user_message = message['message']

    # Load saved knowledge
    if not os.path.exists("knowledge_base.txt"):
        return {"reply": "Knowledge base is empty."}
    
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()

    # Split knowledge into chunks
    paragraphs = knowledge.split("\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return {"reply": "Knowledge base is empty."}

    # Create embeddings
    para_embeddings = embedder.encode(paragraphs)
    question_embedding = embedder.encode([user_message])[0]

    # Find most similar paragraph
    similarities = cosine_similarity([question_embedding], para_embeddings)
    best_idx = similarities.argmax()
    best_paragraph = paragraphs[best_idx]

    # Prepare prompt
    prompt = f"""Use the following knowledge to answer the question:

Knowledge:
{best_paragraph}

Question:
{user_message}

Answer:"""

    # Call Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)

    reply_text = response.text.strip()

    return {"reply": reply_text}
