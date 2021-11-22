"""
Endpoints for delivery agent's pov
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
    jsonify
)

from app.helper import get_pg_conn, token_required

da_bp = Blueprint('da', __name__)

@da_bp.route('/signup/da', methods=['POST'])
def signup():
    """
    Sign up/register a new user

    user details in the form
    {
        "name": ,
        "email": ,
        "password": , (hashed?)
        "phone": ,
        "addr": , -> optional
    }
    """
    user_details = request.json
    public_id = str(uuid.uuid4())

    # Check if necessary fields in post request
    if not ({'email', 'phone', 'name', 'password'} <= user_details.keys()):
        response = Response(
            response=json.dumps({
                "message": "Missing a required parameter (email, phone, name or password)",
            }), 
            content_type='application/json',
            status=400
        )
        return response

    # Make sure phone number can be converted to int
    phone = None
    try:
        phone = int(user_details['phone'])
    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Phone number not a valid phone number",
            }), 
            content_type='application/json',
            status=400
        )
        return response

    # Check if email already registered (we will use 
    # only email and not phone number) for simplicity
    con = get_pg_conn()

    cur = con.cursor(cursor_factory=RealDictCursor)
    email = user_details['email']
    # Check if user already exists
    query = f"""SELECT * FROM CUSTOMER 
        WHERE custemail = '{email}';
    """
    cur.execute(query)
    
    if cur.fetchone() is None:
        if 'addr' in user_details.keys():
            addr = user_details['addr']
        else:
            addr = 'null'

        # First create a wallet entry
        query = f"""INSERT INTO WALLET VALUES (
            default, 0) RETURNING WID
        ;"""
        cur.execute(query)
        wid = cur.fetchone()['wid']
        
        # Insert new user into customer
        query = f"""INSERT INTO CUSTOMER VALUES (
            default, {wid}, null, {phone}, 
            '{addr}', '{user_details['name']}', '{user_details['email']}'
        );"""
        cur.execute(query)
        
        # Insert into app_users
        query = f"""INSERT INTO APP_USERS VALUES (
            '{public_id}',
            '{user_details['email']}',
            '{user_details['password']}',
            'customer'
        );"""
        cur.execute(query)

        # Commit changes
        con.commit()

        # Return the customer record inserted
        query = f"""SELECT CUSTPHONE, CUSTADDR, CUSTNAME, CUSTEMAIL FROM CUSTOMER 
            WHERE CUSTEMAIL = '{user_details['email']}';
        """
        cur.execute(query)        
        item = cur.fetchone()
        response = Response(
            response=json.dumps(item, indent=2),
            mimetype='application/json',
            status=200
        )

    else:
        response = Response(
            response=json.dumps({
                "message": "User already exists. Please sign in.",
            }), 
            content_type='application/json',
            status=400
        )

    cur.close()
    con.close()
    return response


@da_bp.route('/signin/customer', methods=['POST'])
def signin():
    """
    Sign in a customer

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
    current_user = cur.fetchone()

    # If user does not exist
    if current_user is None:
        response = Response(
            response=json.dumps({
                "message": "User does not exist. Please sign up.",
            }), 
            content_type='application/json',
            status=400
        )
        return response

    if current_user['password'] == data['password']:
        # if check_password_hash(current_user.password, data['password']):  
        token = jwt.encode(
            {
                'public_id': current_user['public_id'], 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 
            os.environ['SECRET_KEY']
        )  
        return jsonify({'token' : token}) 

    response = Response(
            response=json.dumps({
                "message": "Could not sign in user.",
            }), 
            content_type='application/json',
            status=400
        )
    return response
    # return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@da_bp.route('/changestatus/delivered', methods=["POST"])
def changestatus():
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    reqbody = request.json 

    daid = reqbody['daid']

    cur.execute(f'''update food_order set ostatus = "DELIVERED" where odaid = {daid} and ostatus = "PICKED UP";''')
    con.commit()

    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps({"message": "Successfully Delivered"}),
        mimetype='application/json'
    )
    return response
