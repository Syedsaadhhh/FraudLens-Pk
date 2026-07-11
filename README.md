# FraudLens PK (Backend)

Welcome to the FraudLens PK Backend project! This is a FastAPI-based REST API designed to analyze text for fraud risk.

## Prerequisites

- Python 3.8+ installed on your system.
- `pip` package manager.

## Setup Instructions

Follow these steps to get the project running on your local machine:

1. **Activate the Virtual Environment (Optional but Recommended)**
   The project already contains a `venv` folder. You can activate it using:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

2. **Install Dependencies**
   Install the required Python packages from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**
   Ensure your `.env` file is properly configured with any required secrets or database credentials (e.g., PostgreSQL credentials).

## Running the Application

To start the FastAPI development server, run the following command from the root of the project:

```bash
uvicorn app.main:app --reload
```

The server will start, and you can access the root endpoint at:
`http://127.0.0.1:8000/`

## API Endpoints

- **Root:** `GET /` - Returns a welcome message.
- **Analyze:** `POST /api/analyze` - Analyzes text for fraud risk. Requires a JSON payload: `{"text": "your text here"}`.

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can explore and test the endpoints directly from your browser:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing the API

The project includes a Python test script to quickly verify the `/api/analyze` endpoint.

1. Ensure the FastAPI server is running (as described above).
2. Open a new terminal window.
3. Run the test script:
   ```bash
   python test_api.py
   ```

This script will send both a valid and an invalid request to the API to ensure it handles them correctly and returns the expected responses.
