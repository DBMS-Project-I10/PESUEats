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
    Sign up/register a new da

    user details in the form
    {
        "name": ,
        "phone": ,
        "password": (hashed?)
    }
    """
    user_details = request.json
    public_id = str(uuid.uuid4())
    con = None
    cur = None

    try:
        # Check if necessary fields in post request
        if not user_details or not ({'phone', 'name', 'password'} <= user_details.keys()):
            response = Response(
                response=json.dumps({
                    "message": "Missing a required parameter (phone, name or password)",
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

        # Check if phone already registered 
        con = get_pg_conn()
        cur = con.cursor(cursor_factory=RealDictCursor)

        # Check if user already exists
        query = f"""SELECT daphone FROM da 
            WHERE daphone = '{phone}';
        """
        cur.execute(query)
        
        if cur.fetchone() is None:

            # First create a wallet entry
            query = f"""INSERT INTO WALLET VALUES (
                default, 0) RETURNING WID
            ;"""
            cur.execute(query)
            wid = cur.fetchone()['wid']
            
            # Insert new user into customer
            # Location is null when created: will
            # only update with diff API
            query = f"""INSERT INTO DA VALUES (
                default, '{phone}', {wid}, '{user_details['name']}', null
            ) RETURNING daid;"""
            cur.execute(query)
            daid = cur.fetchone()['daid']

            # Insert into app_users
            query = f"""INSERT INTO APP_USERS VALUES (
                '{public_id}',
                '{daid}',
                '{user_details['password']}',
                'da'
            );"""
            cur.execute(query)

            # Commit changes
            con.commit()

            # Return the customer record inserted
            query = f"""SELECT daphone, daname FROM da 
                WHERE daphone = '{phone}';
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
                "message": "Delivery agent already exists. Please sign in.",
            }), 
            content_type='application/json',
            status=400
        )
    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Error in request body.",
            }), 
            content_type='application/json',
            status=400
        )

    if cur is not None:
        cur.close()
    if con is not None:
        con.close()
    return response


@da_bp.route('/signin/da', methods=['POST'])
def signin():
    """
    Sign in a delivery agent

    user details in the form
    {
        "username": (phone number),
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

    query = f"""SELECT daid FROM da 
    WHERE daphone='{data['username']}';
    """
    cur.execute(query)

    da = cur.fetchone()
    daid = None

    # If user does not exist
    if da is None or da['daid'] is None:
        response = Response(
            response=json.dumps({
                "message": "User does not exist. Please sign up.",
            }), 
            content_type='application/json',
            status=400
        )
        return response

    else:
        daid = da['daid']

    query = f"""SELECT * FROM app_users 
    WHERE username={daid};
    """

    cur.execute(query)
    current_user = cur.fetchone()

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
                "message": "Incorrect username or password.",
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
