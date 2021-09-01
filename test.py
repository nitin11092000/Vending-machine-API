import requests

BASE = "http://127.0.0.1:5000/"

#sending request to initalise the items in the vending machine
response = requests.put(BASE + "item", {"choice":2})
print(response.json())

input()
#sending request to create a new billing
response = requests.put(BASE + "order", {"quantity1":10, "quantity2":5, "quantity3":15, "one":1115, "two":0, "five":0, "ten":0, "fifteen":0, "twentyfive":0})
print(response.json())

