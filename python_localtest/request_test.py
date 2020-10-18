import requests
import json

url = "https://jsonplaceholder.typicode.com/todos/1"

res = requests.get(url)
data = res.json()

print(data['completed'])