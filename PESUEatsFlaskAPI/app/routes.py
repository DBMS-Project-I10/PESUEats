from psycopg2.extras import RealDictCursor
from flask import Blueprint, request, json, Response

from app.helper import get_pg_conn

#  url_prefix='/api'

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def hello():
    return 'Welcome to PESU Eats API!'

@api_bp.route('/restaurants')
def get_restaurants():
    """
    /restaurants
    """
    con = get_pg_conn()
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

@api_bp.route('/menuitems')
def get_menuitems():
    """
    /menuitems
    /menuitems?rid={}
    """
    con = get_pg_conn()
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


@api_bp.route('/cartinfo')
def get_cart_info():
    """
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cartid = request.args.get('cartid')

    if cartid is None:
        cur.execute("SELECT * FROM CART;")
    
    else:
        cur.execute(f"SELECT * FROM CART WHERE CartId = {cartid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response
    return json.dumps(items, indent=2)


@api_bp.route('/menuitemincarts')
def get_menuitemincarts():
    """
    /menuitemincarts

    /menuitemincarts?cartid=<cartid>
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cartid = request.args.get('cartid')
    if cartid is None:
        cur.execute("SELECT * FROM MENU_ITEM_IN_CART;")
    
    else:
        cur.execute(f"SELECT * FROM MENU_ITEM_IN_CART WHERE MICartId = {cartid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response
    return json.dumps(items, indent=2)


@api_bp.route('/customer')
def get_customer():
    """
    /customer

    /customer?cid=<cid>

    /customer?cname=<cname>
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cid = request.args.get('cid')
    cname = request.args.get('cname')

    if cid is None and cname is None:
        cur.execute("SELECT * FROM CUSTOMER;")
    
    elif cname is None:
        cur.execute(f"SELECT * FROM CUSTOMER WHERE CustId = {cid};")
    
    else:
        cur.execute(f"SELECT * FROM CUSTOMER WHERE CustName = '{cname}';")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

    return json.dumps(items, indent=2)
    

@api_bp.route('/foodorders')
def get_foodorders():
    """
    /foodorders
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM FOOD_ORDER;")
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


@api_bp.route('/ordertransactions')
def get_ordertransactions():
    """
    /ordertransactions
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ORDER_TRANSACTION;")
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


@api_bp.route('/deliveryagent')
def get_da():
    """
    /deliveryagent
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    daid = request.args.get('daid')
    daname = request.args.get('daname')

    if daid is None and daname is None:
        cur.execute("SELECT * FROM DELIVERY_AGENT;")
    
    elif daname is None:
        cur.execute(f"SELECT * FROM DELIVERY_AGENT WHERE CustId = {daid};")
    
    else:
        cur.execute(f"SELECT * FROM DELIVERY_AGENT WHERE CustName = '{daname}';")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

# TODO: needs auth
@api_bp.route('/signup', methods=['POST'])
def signup():
    """
    user details in the form
    {
        "name": ,
        "email": ,
        "password": , (hashed?)
        "phone": ,
        "addr": ,
    }

    TODO: "loc": , (WKT?)
    """
    user_details = request.json

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
    # TODO: add roles to pg con?
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
        
        # Insert into app users
        # TODO: add custom roles?
        query = f"""INSERT INTO APP_USERS VALUES (
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

@api_bp.route('/addtocart', methods=["POST"])
def addtocart():
    reqbody = request.json 
    con = get_pg_conn()
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

@api_bp.route('/showcart')
def showcart():
    con = get_pg_conn()
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

@api_bp.route('/placeorder', methods=["POST"])
def placeorder():
    con = get_pg_conn()
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




    
