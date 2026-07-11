import urllib.request
import urllib.error
import json

URL = "http://127.0.0.1:8000/api/analyze"

def test_valid_request():
    print("Testing valid POST request...")
    data = json.dumps({"text": "Urgent: Please share your OTP to verify your account immediately!"}).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            print(f"Status Code: {status}")
            print("Response Body:")
            print(json.dumps(json.loads(body), indent=2))
            assert status == 200
            assert "riskLevel" in body
            print("Valid request test passed!\n")
    except Exception as e:
        print(f"Valid request test failed: {e}\n")

def test_empty_request():
    print("Testing invalid/empty POST request...")
    data = json.dumps({"text": ""}).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            print(f"Unexpected Success - Status Code: {status}")
            print(body)
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        print(f"Status Code: {status}")
        print("Response Body:")
        print(json.dumps(json.loads(body), indent=2))
        assert status == 400
        assert "detail" in body
        print("Empty request test passed!\n")
    except Exception as e:
        print(f"Empty request test failed: {e}\n")

if __name__ == "__main__":
    test_valid_request()
    test_empty_request()
