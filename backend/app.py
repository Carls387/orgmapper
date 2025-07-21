from flask import Flask, redirect, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

CLIENT_ID = "78kgr4jg9aw2gm"
CLIENT_SECRET = "WPL_AP1.CjhUh2deVtOPiUZ1.EXWKMg=="
REDIRECT_URI = "http://localhost:5000/linkedin/callback"


@app.route('/')
def home():
    return '<a href="/linkedin/login">Connect with LinkedIn</a>'


@app.route('/linkedin/login')
def linkedin_login():
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress",
        "state": "abc123"
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)


@app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    if not code:
        return "Error: no code received", 400

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(token_url, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    if response.status_code != 200:
        return f"Error fetching access token: {response.text}", 400

    access_token = response.json().get("access_token")
    return redirect(f"/linkedin/profile?token={access_token}")


@app.route('/linkedin/profile')
def linkedin_profile():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400

    profile_url = "https://api.linkedin.com/v2/me"
    headers = {"Authorization": f"Bearer {token}"}
    profile = requests.get(profile_url, headers=headers)

    if profile.status_code != 200:
        return f"Error fetching profile: {profile.text}", 400

    return jsonify(profile.json())


@app.route('/linkedin/validate_token')
def validate_token():
    token = request.args.get('token')
    if not token:
        return "Missing token", 400

    introspect_url = "https://www.linkedin.com/oauth/v2/introspectToken"
    response = requests.post(
        introspect_url,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "token": token
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
