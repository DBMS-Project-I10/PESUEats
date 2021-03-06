# Flask app

1. Install dependencies (remember to create a venv)

   ```shell
   pip install -r requirements.txt
   ```

2. Configurate the app by editing `config.ini`

3. Start the flask app server by running

   ```shell
   sh run.sh
   ```

4. If you want to setup your initial PostgresqlDB configuration, set `init` to `true` in `config.ini`, like this:

   ```shell
   [APP_CONFIG]
   init=false
   ```

   After that, just run `run.sh` (mac) or `run.ps1` (windows) to setup the DB at startup.

> DO NOT forget to set it to `false` after your DB ahs been setup!

## TODO

"Unimportant todos":

1. logout to invalidate token
2. Document admin

> Refer Python files for more todos

## Major functionality Summary

(based on minutes of meeting)

Common Views:  
- My profile: View, Update  
- Wallet: View transactions, add  
- order history: see prev orders, cart order  

Specific Views:  
1. Customer  
   restaurant: addtocart, change quantity, empty cart, remove  
   My order: view order, showcart  
2. Restaurant  
   menu: add, delete, update  
   current order: view cart, view order details, two buttons: start prep, handover order | ,   
3. da  
   current delivery: view order, button: delivered
4. Admin  
   all tables to view




## Endpoints

### General endpoints

1. Sign in an existing user

   - Endpoint: `/signin`
   - Token: `not required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "username": "email@email.com:required:string",
         "password": "password:required:string"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "token": "token",
         "role": "customer/da/restaurant"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

2. Get current orders

   - Endpoint: `/orders/current`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      {
         "oid": "order id",
         "ofromrid": "restaurant id",
         "odaid": "da id",
         "otocartid": "cart id",
         "otocartcustid": "customer id",
         "oeta": "timestamp",
         "ostatus": "order status",
         "oplaceddatetime": "timestamp"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

3. Get previous orders

   - Endpoint: `/orders/history`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      {
         "oid": "order id",
         "ofromrid": "restaurant id",
         "odaid": "da id",
         "otocartid": "cart id",
         "otocartcustid": "customer id",
         "oeta": "timestamp",
         "ostatus": "order status",
         "oplaceddatetime": "timestamp"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

4. Get user profile

   - Endpoint: `/myprofile`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      {
         "name": "name",
         "email": "email"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

5. Get all menu items of rest

   - Endpoint: `/restmenuitems`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      [
         {
            "icategory": "Tacos",
            "idescription": "",
            "iid": 22,
            "iinmenurid": 9,
            "iname": "Veg Taco",
            "iprice": 100.0
         }
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

### Customer endpoints

1. Sign up a new customer

   - Endpoint: `/signup/customer`
   - Token: `not required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "name": "name:required:string",               
         "email": "email@email.com:required:string",
         "password": "password:required:string",     
         "phone": "1111111111:required:string",
         "addr": "address:optional:string"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "custaddr": "address",
         "custemail": "email@email.com",
         "custname": "name",
         "custphone": "1111111111"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

2. Add an item to cart

   - Endpoint: `/addtocart`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "itemid": "itemid:required:int",
         "cartid": "cartid:required:int"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "cartid": 1,
         "message": "Successfully added to cart"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

3. Remove an item from cart

   - Endpoint: `/removefromcart`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "itemid": "itemid:required:int",
         "cartid": "cartid:required:int"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "message": "Successfully removed from cart"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

4. Show all items in a cart

   - Endpoint: `/showcart?cartid=<cartid>`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "iid": "item id",
            "iname": "item name",
            "iprice": "item price",
            "miquantity": "quantity"
         },
         {
            "and so on": ""
         }
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

5. Place order

   - Endpoint: `/placeorder`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "cartid": "cartid:required:int"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "message": "Successfully placed order <oid>"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

6. Get a list of all the restaurants

   - Endpoint: `/restaurants`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "rcuisine": "Burgers",
            "rhaswid": 1,
            "rid": 1,
            "rlocation": "12.9716 N, 77.5946 E",
            "rname": "McDonalds",
            "rrating": 4.0
         },
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

7. Get all the menu items of all restaurants

   - Endpoint: `/menuitems`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "icategory": "Classic Burgers",
            "idescription": "desc",
            "iid": 1,
            "iinmenurid": 1,
            "iname": "McVeggie Burger",
            "iprice": 100.0
         },
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

8. Get all the menu items of a single restaurant

   - Endpoint: `/menuitems?rid={rid}`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "icategory": "Classic Burgers",
            "idescription": "desc",
            "iid": 1,
            "iinmenurid": 1,
            "iname": "McVeggie Burger",
            "iprice": 100.0
         },
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

9. Get cart id 
   - Endpoint: `/getcartid`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      {
         "cartid": 1
      },
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

10. Create new cart 
   - Endpoint: `/createnewcart`
   - Token: `required`
   - Method: `POST`
   - On success: `Status 200`

      ```json
      {
         "message": "Successfully created cart", "cartid": 1
      },
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```
### Restaurant endpoints

1. Sign up a new restaurant

   - Endpoint: `/signup/restaurant`
   - Token: `not required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "name": "name:required:string",               
         "email": "email@email.com:required:string",
         "password": "password:required:string",     
         "location": "location:required:string",
         "cuisine": "cuisine:optional:string"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "rname": "restaurant name",
         "remail": "restaurant email",
         "rlocation": "restaurant location",
         "rcuisine": "restaurant cuisine"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

2. Change status to `PREPARING`
   - Endpoint: `/changestatus/preparing`
   - Token: `required`
   - Method: `POST`

   - On success: `Status 200`

      ```json
      {
         "message": "Successfully Delivered"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

3. Change status to `PICKED UP`
   - Endpoint: `/changestatus/preparing`
   - Token: `required`
   - Method: `POST`

   - On success: `Status 200`

      ```json
      {
         "message": "Successfully Delivered"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

4. Add a new menu item

   - Endpoint: `/addmenuitem`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "itemname": "itemname:required:string",               
         "price": "price:required:float",
         "desc": "desc:required:string",     
         "category": "category:required:string"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "iid": 1,
         "icategory": "Dessert",
         "idescription": "Cold dessert",
         "iname": "Ice cream",
         "iprice": 12.25
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

5. Delete menu item from restaurant

   - Endpoint: `/delmenuitem?iid=<iid>`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200` (deleted item)

      ```json
      {
         "icategory": "Dessert",
         "idescription": "Cold dessert",
         "iname": "Ice cream",
         "iprice": 12.25
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

6. Show all active orders of a restaurant

   - Endpoint: `/restactivefoodorders`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "odaid": 4,
            "oeta": null,
            "ofromrid": 9,
            "oid": 1,
            "oplaceddatetime": "Wed, 08 Dec 2021 18:43:41 GMT",
            "ostatus": "PLACED",
            "otocartcustid": 10,
            "otocartid": 1
         },
         {
            "and_so_on": ""
         }
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

7. Show order history of a restaurant

   - Endpoint: `/resthistory`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      [
         {
            "odaid": 4,
            "oeta": null,
            "ofromrid": 9,
            "oid": 1,
            "oplaceddatetime": "Wed, 08 Dec 2021 18:43:41 GMT",
            "ostatus": "DELIVERED",
            "otocartcustid": 10,
            "otocartid": 1
         },
         {
            "and_so_on": ""
         }
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

### Delivery Agent endpoints

1. Sign up a new delivery agent

   - Endpoint: `/signup/da`
   - Token: `not required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "name": "name:required:string",               
         "email": "email@email.com:required:string",
         "password": "password:required:string"
      }
      ```

   - On success: `Status 200`

      ```json
      {
         "daemail": "da email",
         "daname": "da name"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

2. Change status to delivered

   - Endpoint: `/changestatus/delivered`
   - Token: `required`
   - Method: `POST`

   - On success: `Status 200`

      ```json
      {
         "message": "Successfully Delivered"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

3. Get current delivery

   - Endpoint: `/daorder`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      {
         "odaid": 9,
         "oeta": null,
         "ofromrid": 9,
         "oid": 1,
         "oplaceddatetime": "Wed, 08 Dec 2021 18:43:41 GMT",
         "ostatus": "PLACED",
         "otocartcustid": 10,
         "otocartid": 1
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

4. Get delivery history

   - Endpoint: `/dahistory`
   - Token: `required`
   - Method: `GET`

   - On success: `Status 200`

      ```json
      [
         {
            "odaid": 9,
            "oeta": null,
            "ofromrid": 9,
            "oid": 1,
            "oplaceddatetime": "Wed, 08 Dec 2021 18:43:41 GMT",
            "ostatus": "DELIVERED",
            "otocartcustid": 10,
            "otocartid": 1
         }
      ]
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```
