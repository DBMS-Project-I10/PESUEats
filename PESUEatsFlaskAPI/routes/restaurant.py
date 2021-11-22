"""
Endpoints for restaurant's pov
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

from app.helper import get_pg_conn, token_required, validate_dict

rest_bp = Blueprint('rest', __name__)


@rest_bp.route('/signup/restaurant', methods=['POST'])
def signup():
    """
    Sign up/register a new customer

    user details in the form
    {
        "name": ,
        "email": ,
        "password": ,
        "location": ,
        "cuisine": ,
    }
    """
    user_details = request.json
    public_id = str(uuid.uuid4())
    con = None
    cur = None

    try:
        # Check if necessary fields in post request
        if (not user_details 
        or not ({'email', 'name', 'password', 'location', 'cuisine'} <= user_details.keys())):
            response = Response(
                response=json.dumps({
                    "message": "Missing a required parameter (email, name, location, cuisine or password)",
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
            query = f"""INSERT INTO RESTAURANT VALUES (
                default, {wid}, '{email}', '{user_details['name']}', '{user_details['location']}', 
                null, '{user_details['cuisine']}'
            ) RETURNING rid;"""
            cur.execute(query)
            daid = cur.fetchone()['rid']

            # Insert into app_users
            query = f"""INSERT INTO APP_USERS VALUES (
                '{public_id}',
                '{email}',
                '{user_details['password']}',
                'restaurant'
            );"""
            cur.execute(query)

            # Commit changes
            con.commit()

            # Return the restaurant record inserted
            query = f"""SELECT rname, remail, rlocation, rcuisine FROM restaurant 
                WHERE remail = '{email}';
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
                "message": "Restaurant already exists. Please sign in.",
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

@rest_bp.route('/changestatus/preparing', methods=["POST"])
@token_required
def changestatustopreparing(cur_user):
    con = get_pg_conn(user = "restaurant", password = "1234")
    cur = con.cursor(cursor_factory=RealDictCursor)
    # reqbody = request.json 

    # daid = reqbody['daid']

    if cur_user['role'] != 'restaurant':
        response = Response(
            response=json.dumps({"message": "Unathorized access"}),
            mimetype='application/json',
            status = 400
        )
        return response
    
    rid = cur_user['rid']
    
    cur.execute(f'''update food_order set ostatus = "PREPARING" where ofromrid = {rid} and ostatus = "PLACED";''')
    con.commit()

    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps({"message": "Successfully updated status"}),
        mimetype='application/json',
        status = 200
    )
    return response

@rest_bp.route('/changestatus/pickedup', methods=["POST"])
@token_required
def changestatustopickedup(cur_user):
    con = get_pg_conn(user = "restaurant", password = "1234")
    cur = con.cursor(cursor_factory=RealDictCursor)
    # reqbody = request.json 

    # daid = reqbody['daid']

    if cur_user['role'] != 'restaurant':
        response = Response(
            response=json.dumps({"message": "Unathorized access"}),
            mimetype='application/json',
            status = 400
        )
        return response
    
    rid = cur_user['rid']
    
    cur.execute(f'''update food_order set ostatus = "PICKED UP" where ofromrid = {rid} and ostatus = "PREPARING";''')
    con.commit()

    cur.close() 
    con.close() 

    response = Response(
        response=json.dumps({"message": "Successfully updated status"}),
        mimetype='application/json',
        status = 200
    )
    return response