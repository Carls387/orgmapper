# backend/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_ENDPOINT = "https://api.example.com/employees"  # Replace with actual API URL

@app.route("/api/search", methods=["GET"])
def search_employees():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company parameter is required"}), 400

    headers = {
        "Client-ID": CLIENT_ID,
        "Client-Secret": CLIENT_SECRET,
        "Accept": "application/json"
    }
    params = {"company": company}

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        employees = response.json()

        # Filter and format the data
        result = [
            {
                "name": emp.get("name"),
                "job_title": emp.get("title"),
                "company": emp.get("company"),
                "linkedin": emp.get("linkedin_url")
            }
            for emp in employees.get("results", [])
        ]
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

