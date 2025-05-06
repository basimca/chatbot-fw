# Document Chat Assistant

A full-stack application that allows users to chat with their documents using AI. The application supports PDF file uploads and URL processing, with a modern React/Next.js frontend and a Python/FastAPI backend.

## Features

- PDF file upload and processing
- URL content scraping and processing
- Real-time chat interface with AI
- Source attribution for responses
- Modern, responsive UI with Tailwind CSS
- Vector-based document storage and retrieval

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Gemini API key

## Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Upload a PDF file by dragging and dropping it into the upload area or clicking to select a file.
2. Enter a URL to process its content.
3. Start chatting with the AI about the uploaded documents.
4. The AI will provide responses based on the content of your documents and include source attributions.

## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── utils.py          # Utility functions
│   ├── vector_store.py   # Vector database integration
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── src/
    │   ├── app/         # Next.js app directory
    │   └── components/  # React components
    └── package.json     # Node.js dependencies
```

## Technologies Used

- Frontend:
  - Next.js
  - React
  - TypeScript
  - Tailwind CSS

- Backend:
  - FastAPI
  - PyMuPDF
  - BeautifulSoup4
  - Playwright
  - ChromaDB
  - Google Gemini API

## License

MIT 