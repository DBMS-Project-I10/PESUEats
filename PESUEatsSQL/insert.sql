\c pesu_eats

-- Wallet Records
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.23);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);
INSERT INTO WALLET VALUES (DEFAULT, 500.0);

-- Restaurant records
INSERT INTO RESTAURANT VALUES (DEFAULT, 1, 'McDonalds', '12.9716 N, 77.5946 E', 4.0, 'Burgers');
INSERT INTO RESTAURANT VALUES (DEFAULT, 2, 'The Taste of Punjab', '12.9716 N, 77.5946 E', 4.8, 'North Indian');
INSERT INTO RESTAURANT VALUES (DEFAULT, 3, 'Udupi Aahar', '12.9716 N, 77.5946 E', 3.2, 'South Indian');
INSERT INTO RESTAURANT VALUES (DEFAULT, 4, 'Dominos Pizza', '12.9716 N, 77.5946 E', 4.4, 'Pizza');
INSERT INTO RESTAURANT VALUES (DEFAULT, 5, 'Pasta Street', '12.9716 N, 77.5946 E', 4.8, 'Italian');
INSERT INTO RESTAURANT VALUES (DEFAULT, 6, 'Milano Ice Creams', '12.9716 N, 77.5946 E', 5.0, 'Desserts');
INSERT INTO RESTAURANT VALUES (DEFAULT, 7, 'Biryani Palace', '12.9716 N, 77.5946 E', 2.5, 'Biryani');
INSERT INTO RESTAURANT VALUES (DEFAULT, 8, 'Starbucks Coffee', '12.9716 N, 77.5946 E', 4.0, 'Beverages');
INSERT INTO RESTAURANT VALUES (DEFAULT, 9, 'California Burrito', '12.9716 N, 77.5946 E', 3.8, 'Mexican');

-- Customer Records
INSERT INTO CUSTOMER VALUES (DEFAULT, 11, '12.9716 N, 77.5946 E', '12345678910', 'JP Nagar 4th Block', 'Vibha', 'vibha@spesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 12, '12.9716 N, 77.5946 E', '23456789101', 'Koramangala 3rd Block', 'Vishruth', 'vishruth@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 13, '12.9716 N, 77.5946 E', '34567891011', 'Malleshwaram 2nd Stage', 'Tarun', 'tarun@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 14, '12.9716 N, 77.5946 E', '34567891011', 'Jayanagar 1st Block', 'Rahul', 'rahul@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 15, '12.9716 N, 77.5946 E', '34567891011', 'RT Nagar 2nd Stage', 'Soumya', 'soumya@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 16, '12.9716 N, 77.5946 E', '34567891011', 'Yelahanka New Town 1st Block', 'Vaibhav', 'vaibhav@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 17, '12.9716 N, 77.5946 E', '34567891011', 'BTM Layout 2nd Stage', 'Ramya', 'ramya@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 18, '12.9716 N, 77.5946 E', '34567891011', 'HSR Layout 4th Sector', 'Vinayak', 'vinayak@pesueats.com');
INSERT INTO CUSTOMER VALUES (DEFAULT, 19, '12.9716 N, 77.5946 E', '34567891011', 'Banashakari 6th Stage', 'Nikhil', 'nikhil@pesueats.com');

-- Delivery Agent Records
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 21, 'Rajkumar', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 22, 'Prakash', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 23, 'Venkatesh', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 24, 'Prassidha', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 25, 'Devaraj', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 26, 'Lokesh', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 27, 'Mahesh', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 28, 'Suresh', '12.9716 N, 77.5946 E');
INSERT INTO DELIVERY_AGENT VALUES (DEFAULT, 29, 'Rakesh', '12.9716 N, 77.5946 E');

-- Menu Item Records
INSERT INTO MENU_ITEM VALUES (DEFAULT, 1, 'McVeggie Burger', 100.0, NULL, 'Classic Burgers');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 1, 'McChicken Burger', 100.0, '', 'Classic Burgers');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 1, 'French Fries', 100.0, '', 'Sides');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 1, 'Coco-Cola 1L', 100.0, '', 'Beverages');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 2, 'Butter Chicken', 100.0, '', 'Curries');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 2, 'Plain Naan', 100.0, '', 'Rotis and Breads');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 2, 'Paneer Tikka', 100.0, '', 'Starters');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 3, 'Masala Dosa', 100.0, '', 'Breakfast Items');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 3, 'Idli Vada', 100.0, '', 'Breakfast Items');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 3, 'BisiBele Bath', 100.0, '', 'Lunch Items');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 4, 'Margerita', 100.0, '', 'Classics');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 4, 'Veggie Supreme', 100.0, '', 'Supreme Pizzas');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 5, 'Arrabiata Penne', 100.0, '', 'Pasta');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 5, 'Spaghetti Alfredo', 100.0, '', 'Pasta');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 6, 'Choco Mocha', 100.0, '', 'Ice Cream');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 6, 'Choco Fudge', 100.0, '', 'Sundae');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 7, 'Paneer Biryani', 100.0, '', 'Veg Biryanis');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 7, 'Chicken Biryani', 100.0, '', 'Non Veg Biryani');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 7, 'Mutton Biryani', 100.0, '', 'Non Veg Biryani');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 8, 'Classic Latte', 100.0, '', 'Hot Coffee');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 8, 'Frappeciono', 100.0, '', 'Cold Coffee');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 9, 'Veg Taco', 100.0, '', 'Tacos');
INSERT INTO MENU_ITEM VALUES (DEFAULT, 9, 'Veg Burrito', 100.0, '', 'Burritos');

-- Cart Records
INSERT INTO CART VALUES(1, 1, 'NOT PLACED', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(1, 2, 'NOT PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(2, 3, 'PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(2, 4, 'PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(2, 5, 'PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(2, 6, 'PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(2, 7, 'PAID', 200.0, 20.0, 25.0);
INSERT INTO CART VALUES(1, 8, 'NOT PLACED', 0.0, 0.0, 0.0);

-- Menu Item in Cart Records
INSERT INTO MENU_ITEM_IN_CART VALUES(1, 1, 1, 2);
INSERT INTO MENU_ITEM_IN_CART VALUES(3, 1, 1, 1);
INSERT INTO MENU_ITEM_IN_CART VALUES(5, 1, 2, 1);
INSERT INTO MENU_ITEM_IN_CART VALUES(6, 1, 2, 5);
INSERT INTO MENU_ITEM_IN_CART VALUES(8, 2, 3, 2);
INSERT INTO MENU_ITEM_IN_CART VALUES(9, 2, 3, 4);
INSERT INTO MENU_ITEM_IN_CART VALUES(15, 2, 4, 1);
INSERT INTO MENU_ITEM_IN_CART VALUES(16, 2, 4, 1);

-- Order Records
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 1, 1, 1, 1, NULL, 'PREPARING', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 2, 2, 1, 2, NULL, 'ENROUTE', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 3, 3, 2, 3, NULL, 'DELIVERED', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 6, 4, 2, 4, NULL, 'PREPARING', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 5, 5, 2, 5, NULL, 'PREPARING', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 7, 6, 2, 6, NULL, 'ENROUTE', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 8, 7, 2, 7, NULL, 'DELIVERED', NULL);
INSERT INTO FOOD_ORDER VALUES(DEFAULT, 1, 8, 1, 8, NULL, 'PREPARING', NULL);

-- Transaction Records
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 11, 1, 200.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 12, 2, 300.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 13, 3, 400.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 14, 6, 50.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 1, 11, 250.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 2, 12, 460.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 3, 13, 2432.0, NULL);
INSERT INTO ORDER_TRANSACTION VALUES(DEFAULT, 6, 14, 204.0, NULL);

