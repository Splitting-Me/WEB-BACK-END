import requests
headers = {
    'Content-Type': 'application/json'
}
requests.post('http://127.0.0.1:5001/user/0x00', headers=headers)