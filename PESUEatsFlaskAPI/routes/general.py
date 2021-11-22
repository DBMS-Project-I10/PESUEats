"""
Endpoints used by all da, cust and rest
"""

import os
import datetime
import uuid
import jwt

from psycopg2.extras import RealDictCursor
from flask import (
    Blueprint, 
    request, 
    json, 
    Response, 
    make_response, 
    jsonify
)

from app.helper import get_pg_conn, appconfig, token_required

#  url_prefix='/api'

general_bp = Blueprint('general', __name__)

@general_bp.route('/orders/current', methods=["GET"])
@token_required
def getcurrentorders(cur_user):
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    
    custid = None 
    daid = None 
    rid = None 

    if cur_user['role'] == 'cust':
        custid = cur_user['custid']
    elif cur_user['role'] == 'rest':
        rid = cur_user['rid'] 
    elif cur_user['role'] == 'da':
        daid = cur_user['daid'] 

    if custid:
        cur.execute(f'''select * from food_order where otocartcustid = {custid} and ostatus != "DELIVERED";''')
    elif rid: 
        cur.execute(f'''select * from food_order where ofromrid = {rid} and ostatus != "DELIVERED";''')
    elif daid: 
        cur.execute(f'''select * from food_order where odaid = {daid} and ostatus != "DELIVERED";''')

    items = cur.fetchall() 
    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

@general_bp.route('/orders/history', methods=["GET"])
@token_required
def getprevorders(cur_user):
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = None 
    daid = None 
    rid = None 

    if cur_user['role'] == 'cust':
        custid = cur_user['custid']
    elif cur_user['role'] == 'rest':
        rid = cur_user['rid'] 
    elif cur_user['role'] == 'da':
        daid = cur_user['daid'] 

    if custid:
        cur.execute(f'''select * from food_order where otocartcustid = {custid} and ostatus = "DELIVERED";''')
    elif rid: 
        cur.execute(f'''select * from food_order where ofromrid = {rid} and ostatus = "DELIVERED";''')
    elif daid: 
        cur.execute(f'''select * from food_order where odaid = {daid} and ostatus = "DELIVERED";''')

    items = cur.fetchall() 
    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


@general_bp.route('/signin', methods=['POST'])
def signin():
    """
    Sign in a user

    user details in the form
    {
        "username": ,
        "password": , (hashed?)
    }
    """
    data = request.json

    if not data or not data['username'] or not data['password']:  
        response = Response(
            response=json.dumps({
                "message": 'Basic realm: "login required"',
            }), 
            content_type='application/json',
            status=400
        )
        return response

    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    query = f"""SELECT * FROM app_users 
    WHERE username='{data['username']}';
    """
    cur.execute(query)
    user = cur.fetchone()

    # If user does not exist
    if user is None:
        response = Response(
            response=json.dumps({
                "message": "User does not exist. Please sign up.",
            }), 
            content_type='application/json',
            status=400
        )
        return response

    
    if user['password'] == data['password']:
        # if check_password_hash(current_user.password, data['password']):  
        token = jwt.encode(
            {
                'public_id': user['public_id'], 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 
            os.environ['SECRET_KEY']
        )  
        return jsonify({
            'token' : token,
            'role': user['roles']
        }) 


    response = Response(
            response=json.dumps({
                "message": "Incorrect username or password.",
            }), 
            content_type='application/json',
            status=400
        )
    return response
    # return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

