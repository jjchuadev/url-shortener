# Gemini Instructions

## About this Project

This is a simple URL shortener web application built with Flask.

-   **Framework**: The backend is built using the [Flask](https://flask.palletsprojects.com/) web framework. The main application logic is in `app.py`.
-   **Frontend**: The user interface is a single HTML page, `templates/index.html`, which uses vanilla JavaScript to interact with the backend. Styling is in `static/main.css`.
-   **Data Storage**: The application uses an in-memory Python dictionary (`url_mapping` in `app.py`) to store the mapping between short URLs and original URLs. **This means that all shortened URLs are lost when the application restarts.**

## Developer Workflow

### Running the Application

To run the development server, use the following command:

```bash
flask --debug run
```

This will start the application in debug mode, which will automatically reload the server when code changes are detected.

### Key Files

-   `app.py`: The core of the application. It contains all the backend logic, including URL routing, short code generation, and redirection.
-   `templates/index.html`: The main and only webpage. It contains the form for submitting URLs and the JavaScript for handling the API request to the backend.
-   `static/main.css`: The stylesheet for the application.

## Architectural Patterns

-   **API**: The frontend communicates with the backend via a simple JSON API. The endpoint `/shorten` (defined in `app.py`) accepts a POST request with a JSON body containing the `long_url` and returns a JSON response with the `short_url`.
-   **Routing**: Flask's `@app.route()` decorator is used to define the application's routes.
    -   `/`: The main page.
    -   `/shorten`: The API endpoint for creating short URLs.
    -   `/<short_code>`: The route for redirecting short URLs to their original destination.
