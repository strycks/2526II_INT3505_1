import requests

url = 'http://127.0.0.1:5000/'

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Connected")
        print("Server replied: " + response.text)
    else:
        print("Error Code:" + response.status_code)
        
except requests.exceptions.ConnectionError:
    print("Failed to connect")