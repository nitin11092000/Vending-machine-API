->Requirements to run the api:

->pip3 install -r requirements.txt

->main.py is the api file and requests can be sent from the test.py file

->To run the server do ->python3 main.py on a terminal.

->To send requests to the api, add the following in the test.py file:

1. To initialise the vending machine:
	result=requests.put(BASE + "item", {choice":1})
print(result.json())

2. To reset the vending machine:
	result=requests.put(BASE + "item", {choice":2})

3. To custom add stocks to the vending machine:
	result=requests.put(BASE + "item", {choice":3, "stockade":<integer>})

->To order items from the machine, add the following to the test.py file:
	
	result=requests.put(BASE +"item", {"quantity1":<integer>,"quantity2:integer","quantity3":<integer>})

Design Assumptions:
->The server will be able to identify the coins inserted into the vending machine without the user telling it.

Limitations and Scope for Improvements:
->The input of what coins the user wants to insert into the vending machine have to be given at the server side, instead of the client side.
->Reusable code to be done at the client's side to send varied requests.

	

