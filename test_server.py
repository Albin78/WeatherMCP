import requests

def test_server():
    try:
        # Test basic connection
        response = requests.get("http://localhost:8000/sse", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text[:500]}...")  # First 500 characters
        
    except requests.exceptions.ConnectionError:
        print("Connection failed - server not running or port not accessible")
    except requests.exceptions.Timeout:
        print(" Request timed out")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    print("Testing server on localhost:8000...")
    test_server()
