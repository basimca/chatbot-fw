from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from utils import (
    extract_text_from_pdf,
    extract_text_from_pdf_plumber,
    scrape_url_content,
    save_uploaded_file,
)

# Load environment variables
load_dotenv()

# Get and validate API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

print(f"API Key found: {api_key[:5]}...")  # Print first 5 chars of API key

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    print("Successfully configured Gemini model")
except Exception as e:
    print(f"Error configuring Gemini: {str(e)}")
    raise

app = FastAPI(title="Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Models
class ChatMessage(BaseModel):
    message: str

class URLInput(BaseModel):
    url: str

class TextInput(BaseModel):
    text: str

# Routes
@app.get("/")
async def read_root():
    return {"message": "API is running"}

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Save the uploaded file
        file_path = save_uploaded_file(await file.read(), file.filename)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        if not text:
            text = extract_text_from_pdf_plumber(file_path)
        
        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "text": text[:1000] + "..." if len(text) > 1000 else text  # Return first 1000 chars
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/url")
async def process_url(url_input: URLInput):
    try:
        # Try with requests first
        text = scrape_url_content(url_input.url)
        if not text:
            # If that fails, try with playwright
            text = scrape_url_content(url_input.url, use_playwright=True)
        
        return {
            "message": "URL processed successfully",
            "url": url_input.url,
            "text": text[:1000] + "..." if len(text) > 1000 else text  # Return first 1000 chars
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/text")
async def process_text(text_input: TextInput):
    try:
        return {
            "message": "Text processed successfully",
            "text": text_input.text[:1000] + "..." if len(text_input.text) > 1000 else text_input.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(message: ChatMessage, request: Request):
    print(f"\n=== New Chat Request ===")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Message received: {message.message}")
    
    try:
        # Generate response using Gemini
        try:
            print("Attempting to generate response with Gemini...")
            response = model.generate_content(
                f"""You are a helpful AI assistant. Please provide a helpful and informative response to the following message:
                
                {message.message}
                
                Response:"""
            )
            
            print(f"Raw response from Gemini: {response}")
            
            if not response or not response.text:
                print("Empty response received from Gemini")
                raise HTTPException(status_code=500, detail="Empty response from Gemini")
            
            print(f"Successfully generated response: {response.text[:100]}...")
            return {
                "response": response.text,
                "sources": []
            }
        except Exception as e:
            print(f"Gemini API error details: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
            
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get response: {str(e)}")

@app.post("/clear")
async def clear_knowledge_base():
    return {"message": "Knowledge base cleared successfully"} 