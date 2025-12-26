# AI Agent

This project is a simple AI-powered assistant that uses the Mistral AI API and a Streamlit user interface. The agent can provide weather forecasts, book recommendations, jokes, dog photos, and trivia to help you plan.

## Project Structure

- `app.py`: The main Streamlit application that provides the user interface.
- `server.py`: A server that exposes tools for the AI agent to use (e.g., getting weather, books, etc.).
- `requirements.txt`: A list of Python dependencies for the project.
- `.env`: A file to store your Mistral API key.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    Create a file named `.env` in the root of the project and add your Mistral API key:
    ```
    MISTRAL_API_KEY=your_mistral_api_key
    ```

## How to Run

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```
