#!/bin/bash
# menu
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza", "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu1.jpg", "price": 300, "details": ["Italian", "Ham", "Pineapple"]}'
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Chicken Tom Yum Pizza", "desc": "Best marinated chicken with pineapple and mushroom on Spicy Lemon sauce. Enjoy our tasty Thai style pizza.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu2.jpg", "price": 350, "details": ["Italian", "Thai", "Chicken", "Mushroom", "Hot"]}'
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Xiaolongbao", "desc": "Chinese steamed bun", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu3.jpg", "price": 200, "details": ["Chinese", "Pork", "Recommended"]}'
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Kimchi", "desc": "Traditional side dish made from salted and fermented vegetables", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu4.jpg", "price": 50, "details": ["Korean", "Radish", "Cabbage"]}'
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Oolong tea", "desc": "Partially fermented tea grown in the Alishan area", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu5.jpg", "price": 30, "details": ["Hot", "Non-alcohol"]}'
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Beer", "desc": "Fantastic flavors and authentic regional appeal beer", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu6.jpg", "price": 60, "details": ["Alcohol"]}'

# bill_order
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Hawaiian Pizza", "quantity": 1, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Kimchi", "quantity": 2, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Kimchi", "quantity": 1, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 2, "name": "Xiaolongbao", "quantity": 1, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 2, "name": "Beer", "quantity": 1 , "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 3, "name": "Oolong tea", "quantity": 1, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 3, "name": "Beer", "quantity": 3, "action": "add"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Hawaiian Pizza", "quantity": 1, "action": "remove"}'
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Kimchi", "quantity": 1, "action": "remove"}'