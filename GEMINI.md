# GEMINI.md

## Project Overview

This project is a web application for analyzing YouTube videos. It consists of a Python Flask backend and a React frontend.

The application provides two main functionalities:

1.  **Mindmap Generation:** It extracts the transcript of a YouTube video and uses the Gemini API to generate an interactive mindmap of the video's content.
2.  **Comment Analysis:** It fetches the comments of a YouTube video and performs sentiment analysis and semantic clustering to identify key themes and topics.

### Backend

The backend is a Flask application that exposes a REST API.

*   **Framework:** Flask
*   **Key Libraries:**
    *   `google-generativeai`: For interacting with the Gemini API.
    *   `transformers`: For Natural Language Processing tasks.
    *   `youtube_transcript_api`: For fetching video transcripts.
    *   `scikit-learn`, `umap-learn`, `hdbscan`: For comment clustering.
    *   `fpdf2`: For generating PDF reports.

### Frontend

The frontend is a React application built with Vite. It appears to be a landing page for the "Comment Sense AI" application.

*   **Framework:** React
*   **Build Tool:** Vite
*   **Key Libraries:**
    *   `react`, `react-dom`

## Building and Running

### Backend

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```
    The backend will be available at `http://localhost:5001`.

### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd comment-sense-ai
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Development Conventions

### Project Structure

*   **`app.py`:** The main Flask application file.
*   **`requirements.txt`:** Python dependencies for the backend.
*   **`templates/`:** Contains the HTML templates for the Flask application.
*   **`comment-sense-ai/`:** The React frontend application.
    *   **`src/`:** Contains the React source code.
    *   **`package.json`:** Node.js dependencies and scripts for the frontend.
*   **`prompt/`:** Contains text files with prompts for the Gemini API.

### API Endpoints

The backend exposes the following API endpoints:

*   `GET /api/prompts`: Lists the available prompts.
*   `POST /api/transcript`: Fetches the transcript of a YouTube video.
*   `POST /api/comments`: Fetches the comments of a YouTube video.
*   `POST /api/gemini`: Calls the Gemini API with a given prompt and transcript.
*   `POST /api/analyze_comments`: Analyzes the comments of a YouTube video.
*   `POST /api/analyze_batch`: Performs batch analysis of comments.
*   `GET /api/export_data`: Exports the data from the comments table.
*   `POST /api/export_pdf`: Exports the analysis results as a PDF file.
