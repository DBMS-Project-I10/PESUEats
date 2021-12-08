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

from app.helper import get_pg_conn, validate_dict, token_required

da_bp = Blueprint('da', __name__)

@da_bp.route('/signup/da', methods=['POST'])
def signup():
    """
    Sign up/register a new da

    user details in the form
    {
        "name": , -> required
        "email": , -> required
        "password": -> required
    }
    """
    user_details = request.json
    public_id = str(uuid.uuid4())
    con = None
    cur = None

    try:
        # Check if necessary fields in post request
        if not user_details or not ({'email', 'name', 'password'} <= user_details.keys()):
            response = Response(
                response=json.dumps({
                    "message": "Missing a required parameter (email, name or password)",
                }), 
                content_type='application/json',
                status=400
            )
            return response

        # Checks if dict has eny empty strings
        validate_dict(user_details)
        
        email = user_details['email']

        # Check if email already registered 
        con = get_pg_conn()
        cur = con.cursor(cursor_factory=RealDictCursor)

        # Check if user already exists
        query = f"""SELECT username FROM app_users 
            WHERE username = '{email}' and roles = 'da';
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
                default, '{email}', {wid}, '{user_details['name']}', null
            ) RETURNING daid;"""
            cur.execute(query)
            daid = cur.fetchone()['daid']

            # Insert into app_users
            query = f"""INSERT INTO APP_USERS VALUES (
                '{public_id}',
                '{email}',
                '{user_details['password']}',
                'da'
            );"""
            cur.execute(query)

            # Commit changes
            con.commit()

            # Return the customer record inserted
            query = f"""SELECT daemail, daname FROM da 
                WHERE daemail = '{email}';
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


@da_bp.route('/changestatus/delivered', methods=["POST"])
@token_required
def changestatus(cur_user):
    con = get_pg_conn(user = "da", password = "1234")
    cur = con.cursor(cursor_factory=RealDictCursor)
    # reqbody = request.json 

    # daid = reqbody['daid']

    if cur_user['role'] != 'da':
        response = Response(
            response=json.dumps({"message": "Unathorized access"}),
            mimetype='application/json',
            status = 400
        )
        return response
    
    daid = cur_user['daid']

    cur.execute(f'''update food_order set ostatus = 'DELIVERED' where odaid = {daid} and ostatus = 'PICKED UP';''')
    con.commit()

    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps({"message": "Successfully Delivered"}),
        mimetype='application/json'
    )
    return response

@da_bp.route('/daorder', methods=["GET"])
@token_required
def getcurrdelivery(cur_da):
    """
    Get da's current delivery
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=cur_da['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        daid = cur_da['daid']


        query = f"""SELECT * FROM FOOD_ORDER WHERE odaid={daid} and ostatus in ('PLACED', 'PREPARING', 'PICKED UP');
        """
        cur.execute(query)        
        orders = cur.fetchone()

        response = Response(
            response=json.dumps(orders, indent=2),
            mimetype='application/json',
            status=200
        )

    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Error in request/params.",
            }), 
            content_type='application/json',
            status=400
        )
        print(e)

    if cur is not None:
        cur.close()
    if con is not None:
        con.close()

    return response

@da_bp.route('/dahistory', methods=["GET"])
@token_required
def getdahistory(cur_da):
    """
    Get da's history
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=cur_da['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        daid = cur_da['daid']


        query = f"""SELECT * FROM FOOD_ORDER WHERE odaid={daid} and ostatus = 'DELIVERED';
        """
        cur.execute(query)        
        orders = cur.fetchall()

        response = Response(
            response=json.dumps(orders, indent=2),
            mimetype='application/json',
            status=200
        )

    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Error in request/params.",
            }), 
            content_type='application/json',
            status=400
        )
        print(e)

    if cur is not None:
        cur.close()
    if con is not None:
        con.close()

    return response
