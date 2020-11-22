from flask import Blueprint, Response, request, redirect, render_template, url_for
import json
import shortuuid
# from .models import Author

payment = Blueprint('payment_service', __name__)

#TODO: add other get routes etc etc. 

temporary_payment_object = {}

@payment.route('/create', methods=["POST"])
def create_payment():
    
    # print(type(request.json), flush=True)
    body_params = request.json
    try:
        # invoice_nr = body_params["invoice_number"]
        transaction_val = body_params["transaction"]["total"]
        transaction_cur = body_params["transaction"]["currency"]
        items = body_params["item_list"]
        payment_id = shortuuid.uuid()
        temporary_payment_object.update({"id": "PAYMENT-" + str(payment_id),"item_list" : items, "total": transaction_val, "currency": transaction_cur})
    except Exception:
        return Response(response=json.dumps({"Error" : "Possibly wrong params"}), status=500, mimetype='application/json')

    
    
    # return redirect(url_for("/approve"), payment_info=temporary_payment_object)
    return Response(status=200)

# @payment.route('/execute')
# def list_authors():
#    """List all authors.     
#    e.g.: GET /authors"""
#    authors = Author.query.all()
#    content = '<p>Authors:</p>'
#    for author in authors:
#        content += '<p>%s</p>' % author.name
#    return content

@payment.route('/approve')
def display_payment_page():

    return render_template("payment.html", payment_info=temporary_payment_object)