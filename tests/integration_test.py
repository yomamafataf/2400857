import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")


def request(path, data=None, content_type=None):
    headers = {"Content-Type": content_type} if content_type else {}
    call = urllib.request.Request(BASE_URL + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(call) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


home_status, home = request("/")
assert home_status == 200
assert 'name="username"' in home and 'name="password"' in home

short_status, short = request(
    "/create-account",
    urllib.parse.urlencode({"username": "short-test", "password": "short"}).encode(),
    "application/x-www-form-urlencoded",
)
assert short_status == 400 and "Create account" in short

common_status, common = request(
    "/api/password-check",
    json.dumps({"password": "password123"}).encode(),
    "application/json",
)
assert common_status == 200 and json.loads(common)["valid"] is False

password = "CI integration passphrase 2400857!"
valid_status, welcome = request(
    "/create-account",
    urllib.parse.urlencode(
        {"username": "integration-test", "password": password}
    ).encode(),
    "application/x-www-form-urlencoded",
)
assert valid_status == 200 and password in welcome and "Log out" in welcome

print("Integration checks passed over HTTP.")
