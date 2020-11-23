from flask import Blueprint, Response, request, redirect, render_template, url_for
import json
import shortuuid
# from .models import Author

payment = Blueprint('payment_service', __name__)

#TODO: add other get routes etc etc. 

temporary_payment_object = {}

@payment.route('/create')
def create_payment():
    
    # print(type(request.json), flush=True)
    body_params = request.json
    try:
        # invoice_nr = body_params["invoice_number"]
        transaction_val = body_params["transaction"]["total"]
        transaction_cur = body_params["transaction"]["currency"]
        items = body_params["item_list"]
        payment_id = shortuuid.uuid()
        total_tax = 0
        for item in items:
            total_tax += float(item["item_price"]) * 0.23 
        temporary_payment_object.update({"id": "PAYMENT-" + str(payment_id),"item_list" : items, "total": transaction_val, "currency": transaction_cur, "total_tax": str(total_tax)})
    except Exception as e:
        return Response(response=json.dumps({"Error" : e}), status=500, mimetype='application/json')


    # return redirect(url_for("/approve"), payment_info=temporary_payment_object)
    return Response(status=200)

@payment.route('/approve')
def display_payment_page():

    return render_template("payment.html", payment_info=temporary_payment_object)


@payment.route('/execute')
def execute_payment():
    body_params = request.json
    try:
        payment_id = body_params["payment_id"]
        # And also credit card data or access token or something?
    except Exception:
        return Response(response=json.dumps({"Error" : "Possibly wrong params"}), status=500, mimetype='application/json')


    return Response(response=json.dumps({"OK" : "Payment executed and approved", "payment_id": payment_id}), status=200, mimetype='application/json')
