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
         "name": "name",               // optional
         "email": "email@email.com",   // required
         "password": "password",       // required
         "phone": "1111111111",        // required
         "addr": "address"             // optional
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
         "username": "email@email.com",   // optional
         "password": "password"          // required
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
         "itemid": 1    // required - id from menu items table
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
