"""
A simple URL shortener application using Flask.

This application provides an API to shorten long URLs and redirects short URLs
to their original long-form counterparts. It uses an in-memory dictionary
for storage, so shortened URLs are not persisted across application restarts.
"""

import logging
import random
import string
from typing import Dict

from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.wrappers import Response

# --- Application Setup ---

app = Flask(__name__)

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Data Storage ---

# In-memory dictionary to store the mapping from short codes to long URLs.
# Note: This is not a production-ready storage solution. For a real-world
# application, consider using a database like SQLite, PostgreSQL, or Redis.
url_mapping: Dict[str, str] = {}


# --- Utility Functions ---


def generate_short_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric short code of a given length.

    Args:
        length: The desired length of the short code. Defaults to 6.

    Returns:
        A random alphanumeric string.
    """
    characters = string.ascii_letters + string.digits
    short_code = "".join(random.choice(characters) for _ in range(length))
    logging.info(f"Generated new short code: {short_code}")
    return short_code


# --- Routes ---


@app.route("/")
def index() -> str:
    """
    Render the main page of the URL shortener.

    Returns:
        The rendered HTML for the index page.
    """
    return render_template("index.html", title="URL Shortener")


@app.route("/shorten", methods=["POST"])
def shorten_url() -> Response:
    """
    API endpoint to shorten a long URL.

    Expects a JSON payload with a "long_url" key.

    Returns:
        A JSON response containing the shortened URL or an error message.
    """
    data = request.get_json()
    if not data or "long_url" not in data:
        logging.warning("Shorten request failed: 'long_url' not found in payload.")
        return jsonify({"error": "Missing 'long_url' in request body"}), 400

    long_url = data["long_url"]
    if not long_url.startswith(("http://", "https://")):
        logging.warning(f"Shorten request failed: Invalid URL format for '{long_url}'.")
        return jsonify({"error": "Invalid URL format. Must start with http:// or https://"}), 400

    # Generate a unique short code
    while True:
        short_code = generate_short_code()
        if short_code not in url_mapping:
            break

    url_mapping[short_code] = long_url
    short_url = f"{request.host_url}{short_code}"
    logging.info(f"Shortened '{long_url}' to '{short_url}'")

    return jsonify({"short_url": short_url})


@app.route("/<string:short_code>")
def redirect_to_url(short_code: str) -> Response:
    """
    Redirect a short code to its corresponding long URL.

    Args:
        short_code: The short code from the URL.

    Returns:
        A redirect response to the long URL if found, otherwise a 404 error.
    """
    long_url = url_mapping.get(short_code)
    if long_url:
        logging.info(f"Redirecting '{short_code}' to '{long_url}'")
        return redirect(long_url)
    else:
        logging.warning(f"Redirect failed: Short code '{short_code}' not found.")
        return Response("URL not found", status=404)
