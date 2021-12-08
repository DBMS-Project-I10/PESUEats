-- psql -a -f create.sql
-- lowercase DB name (will need to enclose in double 
-- quotes for capital)

DROP DATABASE IF EXISTS pesu_eats;
CREATE DATABASE pesu_eats;

\c pesu_eats

-- Generic fields
CREATE DOMAIN NAME_FIELD AS VARCHAR(25);
CREATE DOMAIN DESCRIPTION_FIELD AS VARCHAR(50) DEFAULT 'No Description';
CREATE DOMAIN STATUS_FIELD AS VARCHAR(10) DEFAULT 'UNKNOWN';
CREATE DOMAIN MONEY_FIELD AS NUMERIC(9, 4) CHECK (VALUE >= 0);
CREATE DOMAIN RATING_FIELD AS NUMERIC(3, 2) CHECK (VALUE <= 5);

-- We will be changing this to a WKT point using PostGIS later
CREATE DOMAIN LOCATION_FIELD AS VARCHAR(25); 
CREATE DOMAIN PHONE_FIELD AS VARCHAR(15);
CREATE DOMAIN ADDR_FIELD AS VARCHAR(60);

-- We can add a regex to check here
CREATE DOMAIN EMAIL_FIELD AS VARCHAR(30);


CREATE TABLE app_users
(
    public_id VARCHAR(50) UNIQUE,
    username EMAIL_FIELD UNIQUE,
    password VARCHAR(30) NOT NULL,
    roles VARCHAR(50)
);

CREATE USER customer WITH PASSWORD '1234';
CREATE USER restaurant WITH PASSWORD '1234' ;
CREATE USER wallet WITH PASSWORD '1234' ;
CREATE USER DA WITH PASSWORD '1234' ;
CREATE USER OrderManager WITH PASSWORD '1234' ;

--roles: customer , restaurant , wallet , DA , OrderManager

-- INSERT INTO app_users VALUES ( 'admin' , '1234' , 'admin' ) ;
-- INSERT INTO app_users VALUES ( 'tarun' , '123' , 'customer' ) ;
-- INSERT INTO app_users VALUES ( 'vibha' , '123' , 'restaurant' ) ;
-- INSERT INTO app_users VALUES ( 'vishruth' , '123' , 'da' ) ;

