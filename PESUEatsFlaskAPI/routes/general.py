"""
Endpoints used by all da, cust and rest
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

from app.helper import get_pg_conn, appconfig, get_da_user, token_required

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