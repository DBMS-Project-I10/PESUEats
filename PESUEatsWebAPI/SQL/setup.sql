-- psql -a -f create.sql
-- lowercase DB name (will need to enclose in double 
-- quotes for capital)

CREATE TABLE app_users
(
    username VARCHAR(15) PRIMARY KEY,
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

