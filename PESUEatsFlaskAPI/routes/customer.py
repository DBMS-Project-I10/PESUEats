"""
Endpoints from a customer's pov
"""

import os
import datetime
import uuid
import jwt

from psycopg2.extras import RealDictCursor, DictCursor
from flask import (
    Blueprint, 
    request, 
    json, 
    Response, 
    make_response, 
    jsonify
)

from app.helper import get_pg_conn, appconfig, get_cust_user, token_required

#  url_prefix='/api'

cust_bp = Blueprint('customer', __name__)



@cust_bp.route('/signup/customer', methods=['POST'])
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
    print(query)
    cur.execute(query)
    
    if cur.fetchone() is None:
        # TODO: update loc, wallet
        if 'addr' in user_details.keys():
            addr = user_details['addr']
        else:
            addr = 'null'

        # First create a wallet entry
        # TODO: psql procedure/function
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
        print(public_id)
        print('not yet failed')
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


@cust_bp.route('/signin/customer', methods=['POST'])
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
     return make_response(
        'could not verify', 
        401, 
        {
            'WWW.Authentication': 'Basic realm: "login required"'
        }
    )

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
    # .decode('UTF-8')
    if current_user['password'] == data['password']:
        # if check_password_hash(current_user.password, auth.password):  
        token = jwt.encode({'public_id': current_user['public_id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.environ['SECRET_KEY'])  
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



@cust_bp.route('/addtocart', methods=["POST"])
@token_required
def addtocart():
    reqbody = request.json 
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    if 'custid' not in reqbody.keys() and 'itemid' not in reqbody.keys():
        response = Response(
            response=json.dumps({"message": "CustId and ItemId not present"}),
            mimetype='application/json',
            status=400
        )
        return response

    # cartid = None
    # Creating new cart if not present
    if 'cartid' not in reqbody.keys():
        cur.execute(f'''update cart set CartStatus = 'INACTIVE' where cartcustid = {reqbody['custid']};''')
        # TODO: Figure out how to add cartids
        # cur.execute(f'''insert into cart values (default, {reqbody.custid}, 'ACTIVE', 0, 0, 0) returning cartid''')
        cur.execute(f'''insert into cart values (1, {reqbody['custid']}, 'ACTIVE', 0, 0, 0) returning cartid''')
        cartid = cur.fetchone()['cartid']
        con.commit() 
    else:
        cartid = reqbody["cartid"] 
    
    if 'quantity' in reqbody.keys():
        quantity = reqbody['quantity']
    else:
        quantity = 1

    #TODO : Figure out how to validate all items being added to cart are from the same restaurant (Might use Triggers and Functions)

    cur.execute(f'insert into menu_item_in_cart values ({reqbody["itemid"]}, {cartid}, {reqbody["custid"]}, {quantity});')

    #TODO IMP: Make a trigger and function to calculate tax amount and total amount of cart and update total amount
    con.commit() 

    cur.close()
    con.close()
    
    response = Response(
            response=json.dumps({"message": "Successfully added to cart", "cartid": cartid}),
            mimetype='application/json',
            status=200
        )
    return response

@cust_bp.route('/removefromcart', methods=["POST"])
@token_required
def removefromcart():
    reqbody = request.json 
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    if 'custid' not in reqbody.keys() or 'itemid' not in reqbody.keys() or 'cartid' not in reqbody.keys():
        response = Response(
            response=json.dumps({"message": "CustId, ItemId or CartId not present"}),
            mimetype='application/json',
            status=400
        )
        return response

    cur.execute(f'delete from menu_item_in_cart where miid = {reqbody["itemid"]} and micartid = {reqbody["cartid"]} and micartcustid = {reqbody["custid"]};')

    #TODO IMP: Make a trigger and function to calculate tax amount and total amount of cart and update total amount
    con.commit() 

    cur.close()
    con.close()
    
    response = Response(
            response=json.dumps({"message": "Successfully removed to cart"}),
            mimetype='application/json',
            status=200
        )
    return response

@cust_bp.route('/showcart')
@token_required
def showcart():
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = request.args.get('custid')
    cartid = request.args.get('cartid')

    if cartid is None and custid is None:
        response = Response(
            response=json.dumps({"message": "CustId and CartId not present"}),
            mimetype='application/json',
            status=400
        )
        return response
        
    if cartid is not None:
        cur.execute(f'SELECT Iid, Iname, Iprice, MIQuantity FROM MENU_ITEM m, MENU_ITEM_IN_CART mc WHERE m.Iid = mc.MIid AND mc.MICartId = {cartid};')
        res = cur.fetchall() 
        response = Response(
            response=json.dumps(res),
            mimetype='application/json',
            status=200
        )
        return response
    
    # Add logic for handling if onlu custid passed and cartid not passed. Find the active cart for that customer 
    else: 
        pass

    cur.close()
    con.close()

@cust_bp.route('/placeorder', methods=["POST"])
@token_required
def placeorder():
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = request.args.get('custid')
    cartid = request.args.get('cartid')

    if cartid is None and custid is None:
        response = Response(
            response=json.dumps({"message": "CustId and CartId not present"}),
            mimetype='application/json',
            status=400
        )
        return response
        
    if cartid is None:
        cartid = cur.execute(f'SELECT cartid FROM CART WHERE cartcustid = {custid} and cartstatus = "ACTIVE";')

    #Get Restaurant Id
    cur.execute(f'SELECT IinMenuRid from MENU_ITEM_IN_CART mc, MENU_ITEM m where micartid = {cartid} and micartcustid = {custid} and mc.miid = m.iid;')
    rid = cur.fetchone()['iinmenurid']

    # Find free DAs 
    cur.execute(f'''SELECT DISTINCT DAId from DELIVERY_AGENT EXCEPT SELECT DISTINCT ODAId FROM FOOD_ORDER WHERE Ostatus != 'DELIVERED'; ''')
    #Pick the first free DA
    daid = cur.fetchone()['daid']

    try:
        cur.execute(f'''insert into food_order values (default, {rid}, {daid}, {cartid}, {custid}, NULL, 'PLACED', NOW()) returning oid;''')
    except Exception:
        response = Response(
            response=json.dumps({"message": "KeyError. The Cartid and Custid is already present"}),
            mimetype='application/json',
            status=400
        )
        return response

    oid = cur.fetchone()['oid']
    cur.execute(f'''update cart set cartstatus = 'INACTIVE' where cartid = {cartid} and cartcustid = {custid};''')
    con.commit() 

    cur.close() 
    con.close() 

    response = Response(
            response=json.dumps({"message": "Successfully placed order", "oid": oid}),
            mimetype='application/json',
            status=200
    )
    return response


@cust_bp.route('/restaurants')
@token_required
def get_restaurants():
    """
    /restaurants
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM RESTAURANT;")
    items = cur.fetchall()
    cur.close()
    con.close()
    
    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

@cust_bp.route('/menuitems')
@token_required
def get_menuitems():
    """
    /menuitems
    /menuitems?rid={}
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    rid = request.args.get('rid')

    if rid is None:
        cur.execute("SELECT * FROM MENU_ITEM;")
    
    else:
        cur.execute(f"SELECT * FROM MENU_ITEM WHERE IinMenuRid = {rid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response
    return json.dumps(items, indent=2)
