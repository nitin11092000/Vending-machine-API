import uuid
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

uuid_obj = uuid.uuid4()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Item Table
class ItemModel(db.Model):
  sno = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String,nullable=False)
  price = db.Column(db.Integer,nullable=False)
  stock = db.Column(db.Integer,nullable=False)
  
#Order Table
class OrderModel(db.Model):
  id = db.Column(db.String, primary_key=True)
  paid = db.Column(db.Integer,nullable=False)
  change = db.Column(db.Integer,nullable=False)
  amount = db.Column(db.Integer,nullable=False)

#before crating the database
#db.create_all()

item_put_args = reqparse.RequestParser()
item_put_args.add_argument("choice", type=int, help="Choice must be given", required=True)
item_put_args.add_argument("sno", type=int, help="Item sno must be mentioned")
item_put_args.add_argument("stockadd", type=int, help="Item Stock must be mentioned")

billing_args = reqparse.RequestParser()
billing_args.add_argument("quantity1", type=int, help="Quantity1 must be mentioned")
billing_args.add_argument("quantity2", type=int, help="Quantity2 must be mentioned")
billing_args.add_argument("quantity3", type=int, help="Quantity3 must be mentioned")
billing_args.add_argument("one", type=int, help="number should be entered")
billing_args.add_argument("two", type=int, help="number should be entered")
billing_args.add_argument("five", type=int, help="number should be entered")
billing_args.add_argument("ten", type=int, help="number should be entered")
billing_args.add_argument("fifteen", type=int, help="number should be entered")
billing_args.add_argument("twentyfive", type=int, help="number should be entered")

class Item(Resource):

  def put(self):

    args = item_put_args.parse_args()
    #for initialising the machine
    if args["choice"]==1:
      i = ItemModel(sno=1, name="Coke", price=25, stock=25)
      db.session.add(i)
      db.session.commit()
      i = ItemModel(sno=2, name="Pepsi", price=32, stock=25)
      db.session.add(i)
      db.session.commit()
      i = ItemModel(sno=3, name="Soda", price=47, stock=25)
      db.session.add(i)
      db.session.commit()
      return "Vending machine initialised!"

    #for resetting the machine to the inital stock
    if args["choice"]==2:
      for i in range(1,4):
        result = ItemModel.query.filter_by(sno=i).first()
        result.stock=25
      db.session.commit()
      return "Vending machine reinitialised!"

    #for setting a custom stock for the machine
    if args["choice"]==3:
      result = ItemModel.query.filter_by(sno=args["sno"]).first()
      if not result:
        abort(404, message="Invalid sno")
      result.stock += args["stockadd"]
      db.session.commit()
      return "Vending machine custom set!"

class Order(Resource):

  def put(self):

    args = billing_args.parse_args()
    o = OrderModel(id=str(uuid.uuid4()), amount=0, paid=0, change=0)
    paid_amount= args["one"] + args["two"] + args["five"] + args["ten"] + args["fifteen"] + args["twentyfive"]
    if args["quantity1"]>0:
      i = ItemModel.query.filter_by(sno=1).first()
      if args["quantity1"]>i.stock:
        abort(404, message="Too many items requested, enter a smaller number")
      o.amount += i.price * args["quantity1"]
      i.stock -= args["quantity1"]
    if args["quantity2"]>0:
      i = ItemModel.query.filter_by(sno=2).first()
      if args["quantity2"]>i.stock:
        abort(404, message="Too many items requested, enter a smaller number")
      o.amount += i.price * args["quantity2"]
      i.stock -= args["quantity2"]
    if args["quantity3"]>0:
      i = ItemModel.query.filter_by(sno=3).first()
      if args["quantity3"]>i.stock:
        abort(404, message="Too many items requested, enter a smaller number")
      o.amount += i.price * args["quantity3"]
      i.stock -= args["quantity3"]
    if paid_amount<o.amount:
      abort(404, message="Paid amount is less than required amount")
    print("Total amount to be paid is " + str(o.amount))
    print("Proceed?")
    cond = str(input())
    if cond=="no":
      return "Bill cancelled"
    o.paid = paid_amount
    o.change = o.paid-o.amount
    print("paid amount = " +str(o.paid))
    print("total amount = " +str(o.amount))
    print("Remaining change = " +str(o.change))
    print("Proceed?")
    cond = str(input())
    if cond=="no":
      print("Processing refund")
      return [args["one"], args["two"], args["five"], args["ten"], args["fifteen"], args["twentyfive"]]
    db.session.add(o)
    db.session.commit()
    return "Collect items"

api.add_resource(Item, "/item")
api.add_resource(Order,"/order")

if __name__ == "__main__":
	app.run(debug=True)