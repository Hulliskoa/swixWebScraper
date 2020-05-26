import requests
import json
file = open('kotlinProducts.json', 'r')
jsondata = json.load(file)
headers = {'Content-type': 'application/json'}
requests.post('http://localhost:8080/api/insert/products', data = json.dumps(jsondata), headers = headers)
