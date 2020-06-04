import requests
import json
file = open('swixProducts.json', 'r')
jsondata = json.load(file)
headers = {'Content-type': 'application/json'}
requests.post('https://repairable-restore.herokuapp.com/api/insert/products', data = json.dumps(jsondata), headers = headers)
