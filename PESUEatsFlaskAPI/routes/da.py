"""
Endpoints for delivery agent's pov
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

da_bp = Blueprint('da', __name__)

# @da_bp.route('/orders/da/current', methods=["GET"])
# def getcurrentorders():
#     con = get_pg_conn()
#     cur = con.cursor(cursor_factory=RealDictCursor)

#     daid = request.args.get('daid')

#     cur.execute(f'''select * from food_order where odaid = {daid} and ostatus != "DELIVERED";''')
#     items = cur.fetchall() 
#     cur.close() 
#     con.close() 

#     response = Response(
#         response=json.dumps(items, indent=2),
#         mimetype='application/json'
#     )
#     return response

# @da_bp.route('/orders/da/history', methods=["GET"])
# def getprevorders():
#     con = get_pg_conn()
#     cur = con.cursor(cursor_factory=RealDictCursor)

#     daid = request.args.get('daid')

#     cur.execute(f'''select * from food_order where odaid = {daid} and ostatus = "DELIVERED";''')
#     items = cur.fetchall() 
#     cur.close() 
#     con.close() 

#     response = Response(
#         response=json.dumps(items, indent=2),
#         mimetype='application/json'
#     )
#     return response

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