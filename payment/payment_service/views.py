from flask import Blueprint, Response, request, redirect, render_template, url_for
import json
import shortuuid
from payment_service.database import *
from payment_service.common import calculateTax

payment = Blueprint('payment_service', __name__)

#TODO: add other get routes etc etc. 

temporary_payment_object = {}
db = Database() 



@payment.route('/create')
def create_payment():
    
    # print(type(request.json), flush=True)
    body_params = request.json
    try:
        # invoice_nr = body_params["invoice_number"]
        client_id = body_params["client_id"]
        transaction_val = body_params["transaction"]["total"]
        transaction_cur = body_params["transaction"]["currency"]
        items = body_params["item_list"]
        payment_id = shortuuid.uuid()
        total_tax = calculateTax(items)
        
        payment = {"id": "PAYMENT-" + str(payment_id),"item_list" : items, "total": transaction_val, "currency": transaction_cur, "total_tax": str(total_tax), "client_id": client_id}
        temporary_payment_object.update(payment)

        if not db.insertPayment(payment):
            return Response(response=json.dumps({"Error" : "Something went wrong while creatinga new payment! Try again!"}), status=500, mimetype='application/json')

        print(db.getPayments(), flush=True)

    except Exception as e:
        return Response(response=json.dumps({"Error" : e}), status=500, mimetype='application/json')


    # return redirect(url_for("/approve"), payment_info=temporary_payment_object)
    return Response(status=200)

@payment.route('/approve/<payment_id>')
def display_payment_page(payment_id):

    # Fetch the payment object from DB
    payment = db.getPayments(payment_id)

    # Check if that exists
    if not payment:
        return Response(response=json.dumps({"Error" : "<payment_id> provided doesn't exist!"}), status=500, mimetype='application/json')


    payment["total_tax"] = calculateTax(payment["item_list"])
    

    return render_template("payment.html", payment_info=payment)


@payment.route('/execute', methods=['POST'])
def execute_payment():
    body_params = request.json

    try:
        access_token = body_params["access_token"]
    except Exception as e:
        print("No access token. Assuming credit card and not RoadRnD funds", flush=True)
        return Response(response=json.dumps({"ERROR" : e}), status=500, mimetype='application/json')

    print(access_token)

    # try:
    #     # payment_id = body_params["payment_id"]
    #     # And also credit card data or access token or something?
    #     print(body_params, flush=True)
        
    # except Exception:
    #     return Response(response=json.dumps({"Error" : "Possibly wrong params"}), status=500, mimetype='application/json')


    return Response(response=json.dumps({"OK" : "Payment executed and approved", "payment_id": access_token}), status=200, mimetype='application/json')
