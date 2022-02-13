import requests

dupa = requests.get("http://127.0.0.1:8080/api", headers={'Authorization': "eyJ0eXAiOiJKVRQiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0NTEwMzQ0LCJpYXQiOjE2NDQ1MTAwNDQsImp0aSI6ImJkNDhlYTE0YzY4MTQ1ZjhiMWIwZGNlZmQzYzU5NTQxIiwidXNlcl9pZCI6Ik5vbmUifQ.PWD3gAa-em538Mxlnoqv2_Judo3FZwZHSkAhR1WlkrU"})
print(dupa.json())