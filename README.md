# Threat-Intelligence

# Description

This project is a simple web-based Threat Intelligence Platform that allows users to check the reputation of IP addresses or domains using the AbuseIPDB API. It provides a quick way to assess if a network identifier has been associated with malicious activities reported by a global community.

## Features

*   **IP/Domain Input:** Accepts either an IPv4 address or a domain name.
*   **Domain Resolution:** Automatically resolves domain names to IP addresses.
*   **AbuseIPDB Integration:** Queries the AbuseIPDB API v2 for threat information.
*   **Reputation Score:** Displays the Abuse Confidence Score (%) for the queried IP.
*   **Last Reported Date:** Shows when the IP was last reported for malicious activity.
*   **Query History:** Stores and displays the last 10 queries made through the platform.
*   **Error Handling:** Provides feedback for invalid inputs or API errors.
*   **Web Interface:** Simple and clean user interface built with Flask, HTML, and CSS.
*   **REST API:** Includes a basic API endpoint for programmatic checks.

## How it Works

1.  The user enters an IP address or domain name via the web interface.
2.  The Flask application (`app.py`) receives the input.
3.  If a domain is entered, it attempts to resolve it to an IP address.
4.  The application sends the IP address to the AbuseIPDB API.
5.  AbuseIPDB returns reputation data (or an error).
6.  The application processes the response and saves the query to `consultas.json`.
7.  Results (or errors) and the recent query history are displayed on the web page.

## Technology Stack

*   **Backend:** Python, Flask
*   **API Interaction:** `requests` library
*   **Frontend:** HTML, CSS, Jinja2 (Flask templating)
*   **External Service:** AbuseIPDB API
*   **Data Storage:** JSON file (`consultas.json`) for query history

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Threat_Intelligence
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Key:**
    *   Open `app.py`.
    *   Replace the placeholder value for `ABUSEIPDB_API_KEY` with your actual AbuseIPDB API key.
    ```python
    # ⚠️ Replace with your real AbuseIPDB key
    ABUSEIPDB_API_KEY = "YOUR_REAL_API_KEY_HERE"
    ```
5.  **Run the application:**
    ```bash
    flask run
    # Or using Gunicorn (as specified in Procfile)
    # gunicorn app:app
    ```
6.  Access the application in your web browser, usually at `http://127.0.0.1:5000`.

## Usage

*   **Web Interface:** Navigate to the application's URL in your browser. Enter an IP address (e.g., `8.8.8.8`) or a domain (e.g., `google.com`) into the input field and click "Check". The results and recent history will be displayed.
*   **API Endpoint:** Send a GET request to `/api/check_ip/<ip_or_domain>`.
    *   Example: `curl http://127.0.0.1:5000/api/check_ip/8.8.8.8`
    *   The API will return JSON data with the results or an error message.
