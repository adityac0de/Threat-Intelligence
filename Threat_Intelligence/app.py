import requests
import socket
import json
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Name of the JSON file where queries will be stored
CONSULTAS_FILE = "consultas.json"

# ⚠️ Replace with your real AbuseIPDB key
ABUSEIPDB_API_KEY = "7652758a92b582f623257d1258cd4512b26ddf7ca4b5d2177bcd9d30578f29fa33fc0737ee25b8a9"

def resolve_domain(domain):
    """Attempts to resolve a domain to an IP. Returns None if not possible."""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def check_ip(ip):
    """Queries IPs on AbuseIPDB and handles response errors."""
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("errors", [{"detail": "Unknown API error"}])[0]["detail"]}

        return data
    except Exception as e:
        return {"error": f"Error querying AbuseIPDB: {str(e)}"}

def save_query(ip, data):
    """Saves the query to the JSON file."""
    try:
        with open(CONSULTAS_FILE, "r") as file:
            queries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        queries = []

    new_query = {
        "ip": ip,
        "result": data,
        "date_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    queries.insert(0, new_query)  # Add to the top
    queries = queries[:10]  # Keep only the last 10 queries

    with open(CONSULTAS_FILE, "w") as file:
        json.dump(queries, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None

    if request.method == "POST":
        user_input = request.form["ip"].strip()

        # If it's a domain, try to resolve to IP
        if not user_input.replace(".", "").isdigit():
            ip = resolve_domain(user_input)
            if not ip:
                error = f"Domain '{user_input}' cannot be resolved to a valid IP. Check if it is accessible."
                print(f"Error: {error}")  # Debugging in logs
        else:
            ip = user_input  # Already an IP, proceed

        print(f"Resolved IP: {ip}")  # Debugging in logs

        if ip:
            data = check_ip(ip)
            if "error" in data:
                error = data["error"]
            else:
                save_query(ip, data)
        else:
            if not error:
                error = "The entered IP is not valid. Please enter a correct IP."

    try:
        with open(CONSULTAS_FILE, "r") as file:
            queries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        queries = []

    return render_template("index.html", data=data, error=error, consultas=queries)

@app.route("/api/check_ip/<ip>")
def api_check_ip(ip):
    resolved_ip = resolve_domain(ip) if not ip.replace(".", "").isdigit() else ip

    if not resolved_ip:
        return jsonify({"error": "Invalid domain or incorrect IP"}), 400

    data = check_ip(resolved_ip)
    if "error" in data:
        return jsonify(data), 400

    save_query(resolved_ip, data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
