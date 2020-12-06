from flask import Blueprint, Response, request, redirect, render_template, url_for
import json
import shortuuid
from payment_service.database import *
from payment_service.common import calculateTax

payment = Blueprint('payment_service', __name__)



db = Database() 

## TODO: create DELETE  for clients
@payment.route('/client/<client_id>', methods=["GET"])
def get_client(client_id):

    client = db.getClients(client_id)

    # Check if that exists
    if not client:
        return Response(response=json.dumps({"Error" : "<client_id> provided doesn't exist!"}), status=500, mimetype='application/json')

    return Response(response=json.dumps(client), status=200, mimetype='application/json')

@payment.route('/client/<client_id>', methods=["PUT"])
def update_client(client_id):

    body_params = request.json
    try:
        client = db.getClients(client_id)
        if not client:
            return Response(response=json.dumps({"Error" : "<client_id> provided doesn't exist!"}), status=500, mimetype='application/json') 
        new_balance = str(float(client["balance"]) + float(body_params["balance"]))
        db.updateClientFunds(client_id, new_balance)
    except Exception as e:
        return Response(response=json.dumps({"Error" : "Something went wrong while updating client balance", "test": e}), status=500, mimetype='application/json')

    return Response(status=200, mimetype='application/json')


@payment.route('/client', methods=["POST"])
def add_client():

    body_params = request.json
    try:
        # invoice_nr = body_params["invoice_number"]
        client_id = body_params["client_id"]
        currency = body_params["currency"]
        
        client = {"id": client_id, "currency": currency}

        if not db.insertClient(client):
            return Response(response=json.dumps({"Error" : "Something went wrong while creatinga new payment! Try again!"}), status=500, mimetype='application/json')

        print(db.getClients(), flush=True)

    except Exception as e:
        return Response(response=json.dumps({"Error" : e}), status=500, mimetype='application/json')


    # return redirect(url_for("/approve"), payment_info=temporary_payment_object)
    return Response(status=200)



@payment.route('/payment/<payment_id>', methods=["GET"])
def get_payment(payment_id):
    payment = db.getPayments(payment_id)

    # Check if that exists
    if not payment:
        return Response(response=json.dumps({"Error" : "<payment_id> provided doesn't exist!"}), status=500, mimetype='application/json')

    return Response(response=json.dumps(payment), status=200, mimetype='application/json')

@payment.route('/payment/<payment_id>', methods=["DELETE"])
def remove_payment(payment_id):

    if not db.deletePayment(payment_id):
        return Response(response=json.dumps({"Error" : "<payment_id> provided doesn't exist!"}), status=500, mimetype='application/json')


    return Response(status=200, mimetype='application/json')
 

@payment.route('/payment', methods=["POST"])
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

        if not db.insertPayment(payment):
            return Response(response=json.dumps({"Error" : "Something went wrong while creatinga new payment! Try again!"}), status=500, mimetype='application/json')

        print(db.getPayments(), flush=True)

    except Exception as e:
        return Response(response=json.dumps({"Error" : e}), status=500, mimetype='application/json')


    # return redirect(url_for("/approve"), payment_info=temporary_payment_object)
    return Response(response=json.dumps({"payment_id": payment["id"]}), status=200)

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
        payment_id = body_params["payment_id"]
    except Exception:
        return Response(response=json.dumps({"Error" : "Possibly wrong params"}), status=500, mimetype='application/json')


    try:
        access_token = body_params["access_token"]
        print("access_token:" + str(access_token), flush=True)
        ## TODO: check access token validity
        ## TODO: Make eventual USD to EUR conversions and vice-versa. Lets assume all EUR for now
        
        # Fetch payment data from db.
        payment = db.getPayments(payment_id)

        # Access client stuff from db.
        client_acc = db.getClients(payment["client_id"])
        if not client_acc:
            return Response(response=json.dumps({"Error" : str(payment["client_id"]) + " doesn't exist!"}), status=500, mimetype='application/json')

        # Check if enough funds, if yes, deduct from one client (and add to eventually other client?) and return OK else return not allowed
        payment_status = 'not_approved'
        if client_acc["currency"] == payment["currency"]:
            new_balance = str(float(client_acc["balance"]) - float(payment["total"]))

            if new_balance >= 0:
                if not db.updateClientFunds(client_acc["id"], new_balance):
                    return Response(response=json.dumps({"Error" : "Couldn't update client balance!"}), status=500, mimetype='application/json')
                payment_status = 'approved'
        else:
            return Response(response=json.dumps({"Error" : "Currencies from client account don't match the payment currency. (Operation not supported yet!)"}), status=500, mimetype='application/json')
    
        # Update payment status to approved or not approved and update the timestamps and return respective
        if not db.updatePaymentStatus(payment_id, payment_status):
            return Response(response=json.dumps({"Error" : "Couldn't update payment status!"}), status=500, mimetype='application/json')
 
        if payment_status == 'not_approved':
            return Response(response=json.dumps({"OK" : "Payment not approved!"}), status=200, mimetype='application/json')
        else:
            return Response(response=json.dumps({"OK" : "Payment executed and approved"}), status=200, mimetype='application/json')


    except Exception:
        print("No access token. Assuming credit card and not RoadRnD funds", flush=True)
        # return Response(response=json.dumps({"ERROR" : e}), status=500, mimetype='application/json')

    ## We assume credit card stuff is always allowed

    ## TODO: return payment status and update times etc
    ## TODO: How does the exterior have access to these responses?
    return Response(response=json.dumps({"OK" : "Payment executed and approved"}), status=200, mimetype='application/json')
