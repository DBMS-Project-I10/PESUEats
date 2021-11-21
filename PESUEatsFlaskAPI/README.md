# Flask app

1. Install dependencies (remember to create a venv)

   ```shell
   pip install -r requirements.txt
   ```

2. Configurate the app by editing `config.ini`

3. Source the environment variables by running

   ```shell
   source variables.sh
   ```

4. Start the flask app server by running

   ```shell
   sh run.sh
   ```

## Endpoints

### Customer endpoints

1. Sign up a new customer

   - Endpoint: `/signup/customer`
   - Token: `not required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "name": "name:optional:string",               
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

2. Sign in an existing customer

   - Endpoint: `/signin/customer`
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
         "token": "token"
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

3. Add an item to cart

   - Endpoint: `/addtocart`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         "itemid": "itemid:required:int"
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

4. Remove an item from cart

   - Endpoint: `/removefromcart`
   - Token: `required`
   - Method: `POST`
   - Form format:

      ```json
      {
         
      }
      ```

   - On success: `Status 200`

      ```json
      {
         
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

5. Show all items in a cart

   - Endpoint: `/showcart`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      {
         
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

6. Place order

   - Endpoint: `/placeorder`
   - Token: `required`
   - Method: `GET`
   - On success: `Status 200`

      ```json
      {
         
      }
      ```

   - On error: `Status 400`

      ```json
      {
         "message": "error message"
      }
      ```

7. Get a list of all the restaurants

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

8. Get all the menu items of all restaurants

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

9. Get all the menu items of a single restaurant

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
