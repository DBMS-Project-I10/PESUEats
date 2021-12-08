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
    Response
)

from app.helper import get_pg_conn, token_required, validate_dict

rest_bp = Blueprint('rest', __name__)


@rest_bp.route('/signup/restaurant', methods=['POST'])
def signup():
    """
    Sign up/register a new restaurant

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
    """
    {
        "oid": "order id"
    }
    """
    con = get_pg_conn(user = "restaurant", password = "1234")
    cur = con.cursor(cursor_factory=RealDictCursor)
    reqbody = request.json 

    try:
        oid = reqbody['oid']
    except:
        response = Response(
            response=json.dumps({"message": "Order ID missing"}),
            mimetype='application/json',
            status = 400
        )
        cur.close() 
        con.close()
        return response
    # daid = reqbody['daid']

    if cur_user['roles'] != 'restaurant':
        response = Response(
            response=json.dumps({"message": "Unauthorized access"}),
            mimetype='application/json',
            status = 400
        )
        cur.close() 
        con.close()
        return response
    
    rid = cur_user['rid']
    
    cur.execute(f'''update food_order set ostatus = 'PREPARING' where ofromrid = {rid} and oid = {oid} and ostatus = 'PLACED' returning *;''')
    updated_record = cur.fetchone()
    con.commit()

    if updated_record is None:
        response = Response(
            response=json.dumps({"message": "No such order exists"}),
            mimetype='application/json',
            status = 200
        )
        cur.close() 
        con.close()
        return response

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
    reqbody = request.json 

    oid = reqbody['oid']

    if cur_user['role'] != 'restaurant':
        response = Response(
            response=json.dumps({"message": "Unathorized access"}),
            mimetype='application/json',
            status = 400
        )
        cur.close() 
        con.close()
        return response
    
    rid = cur_user['rid']
    
    cur.execute(f'''update food_order set ostatus = 'PICKED UP' where ofromrid = {rid} and ostatus = 'PREPARING' and oid = {oid};''')
    con.commit()

    cur.close() 
    con.close()

    response = Response(
        response=json.dumps({"message": "Successfully updated status"}),
        mimetype='application/json',
        status = 200
    )
    return response
    
@rest_bp.route('/addmenuitem', methods=["POST"])
@token_required
def addmenuitem(current_rest):
    """
    Add a menu item to the restaurant's menu items

    {
        "itemname": 
        "price":
        "desc":
        "category":
    }
    """

    con = None
    cur = None

    menu_data = request.json

    try:
        con = get_pg_conn(user=current_rest['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        rid = current_rest['rid']

        price = menu_data['price']

        if type(price) == str:
            price = float(price)

        query = f"""INSERT INTO MENU_ITEM VALUES (
            default, {rid}, '{menu_data['itemname']}', 
            {price}, '{menu_data['desc']}',
            '{menu_data['category']}'
        ) RETURNING Iid, IName, IPrice, IDescription, ICategory;
        """
        cur.execute(query)
        item = cur.fetchone()
        con.commit() 

        response = Response(
            response=json.dumps(item, indent=2),
            mimetype='application/json',
            status=200
        )
    
    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Error in request body/not authorised.",
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

@rest_bp.route('/delmenuitem', methods=["GET"])
@token_required
def delmenuitem(current_rest):
    """
    Delete a menu item from the restaurant's menu items

    /delmenuitem?iid=<iid>
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=current_rest['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        rid = current_rest['rid']

        iid = request.args.get("iid")

        query = f"""SELECT IName, IPrice, IDescription, ICategory from
        MENU_ITEM WHERE IinMenuRid = {rid} and Iid = {iid}
        ;
        """
        cur.execute(query)        
        item = cur.fetchone()

        query = f"""DELETE FROM MENU_ITEM WHERE IinMenuRid = {rid} and Iid = {iid};"""
        cur.execute(query)     
        con.commit()    
        
        response = Response(
            response=json.dumps(item, indent=2),
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

@rest_bp.route('/restactivefoodorders', methods=["GET"])
@token_required
def getactiveorders(current_rest):
    """
    Get all active food orders for a restaurant
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=current_rest['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        rid = current_rest['rid']


        query = f"""SELECT * FROM FOOD_ORDER WHERE ofromrid={rid} and ostatus in ('PLACED', 'PREPARING');
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

@rest_bp.route('/resthistory', methods=["GET"])
@token_required
def getorderhistory(current_rest):
    """
    Get order history for a restaurant
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=current_rest['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        rid = current_rest['rid']


        query = f"""SELECT * FROM FOOD_ORDER WHERE ofromrid={rid} and ostatus = 'DELIVERED';
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

@rest_bp.route('/restmenuitems', methods=["GET"])
@token_required
def restmenuitems(current_rest):
    """
    Get all menu items in a restaurant
    """

    con = None
    cur = None


    try:
        con = get_pg_conn(user=current_rest['roles'])
        cur = con.cursor(cursor_factory=RealDictCursor)
        rid = current_rest['rid']

        iid = request.args.get("iid")

        query = f"""SELECT * from MENU_ITEM WHERE IinMenuRid = {rid};
        """
        cur.execute(query)        
        items = cur.fetchall()

        
        response = Response(
            response=json.dumps(items, indent=2),
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