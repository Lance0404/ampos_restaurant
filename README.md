# ampos_restaurant

### Tools
* framework: flask
* db: postgresql
* orm: sqlalchemy

### Env spec
* CPU 4, RAM 3G
* docker installed

### Deployment
* run bash script
* for the first time (recreate db)
```shell
sudo ./refresh.sh drop
```
* only to restart (db kept)
```shell
sudo ./refresh.sh
```

### Monitor log
* log file was mounted out
```shell
tail -f /var/log/ampos/web.log
```
* w/ docker-compose 
```shell
sudo docker-compose logs -f --tail=10
```

### Schema design
* in ar.models

--- 
### Operations 


#### Insert New Item in Menu
**Request**
* Endpoint: `POST /v1/menu`
* Header:
    - Content-Type: application/json

| Parameter | Type | Required | Example |
|:---------:|:----:|:----------------:|:-------:|
| `name` | str | Y | see below |
| `desc` | str | N | see below |
| `image` | str | N | see below |
| `price` | str | Y | see below |
| `details` | array of str | N | see below |

**Example**
```shell
curl -v -X POST 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza", "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu1.jpg", "price": 300, "details": ["Italian", "Ham", "Pineapple"]}'
```
```json
{
  "msg": "ok",
  "status": true
}
```

#### Update Item in Menu
**Request**
* Endpoint: `PUT /v1/menu`
* Header:
    - Content-Type: application/json

| Parameter | Type | Required | Example |
|:---------:|:----:|:----------------:|:-------:|
| `name` | str | Y | see below |
| `desc` | str | N | see below |
| `image` | str | N | see below |
| `price` | str | Y | see below |
| `details` | array of str | N | see below |

**Example**
```shell
curl -v -X PUT 'http://localhost/v1/menu' -H 'Content-Type: application/json' -d '{"name": "Hawaiian Pizza", "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.", "image": "https://s3-ap-southeast-1.amazonaws.com/interview.ampostech.com/backend/restaurant/menu1.jpg", "price": 300, "details": ["Italian", "Ham", "Pineapple"]}'
```
```json
{
  "msg": "ok",
  "status": true
}
```

#### Search Item from Menu (w/ pagination)
**Request**
* Endpoint: `GET /v1/menu/search`
* Header:
    - Content-Type: application/json

| Parameter | Type | Required | Default | Example |
|:---------:|:----:|:--------:|:-------:|:-------:|
| `name` | str | N | | see below |
| `desc` | str | N | |  see below |
| `details` | str | N | | see below |
| `limit` | str | N | 10 | see below |
| `page` | str | N | 1 | see below |

**Example**
```shell
# search for all items in menu
curl -v -X GET 'http://localhost/v1/menu/search'
# search against title
curl -v -X GET 'http://localhost/v1/menu/search?name=Hawaiian'
# search against title, desc and details
curl -v -X GET 'http://localhost/v1/menu/search?name=Hawaiian&desc=toppings&details=Ham'
# search with pagination
curl -v -X GET 'http://localhost/v1/menu/search?name=Hawaiian&desc=toppings&details=Ham&limit=1&page=1'
```
```json
{
  "data": [
    {
      "_mtime": "Fri, 26 Apr 2019 10:23:30 GMT",
      "desc": "All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.",
      "details": [
        "italian",
        "ham",
        "pineapple"
      ],
      "id": 1,
      "image": "https:\/\/s3-ap-southeast-1.amazonaws.com\/interview.ampostech.com\/backend\/restaurant\/menu1.jpg",
      "name": "Hawaiian Pizza",
      "name_hash": "6ba4e2b2644740b1ded79d77425954e1657abb40",
      "price": 300
    }
  ],
  "msg": "ok",
  "status": true
}
```

#### Add or Remove bill order
* all records were kept in db

**Request**
* Endpoint: `POST /v1/billorder`
* Header:
    - Content-Type: application/json

| Parameter | Type | Required | Example |
|:---------:|:----:|:----------------:|:-------:|
| `bill_no` | str | Y | see below |
| `name` | str | Y | see below |
| `quantity` | str | Y | see below |
| `action` | str | Y | see below |

**Example**
```shell
# add
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Hawaiian Pizza", "quantity": 1, "action": "add"}'
# remove
curl -v -X POST 'http://localhost/v1/billorder' -H 'Content-Type: application/json' -d '{"bill_no": 1, "name": "Hawaiian Pizza", "quantity": 1, "action": "remove"}'
```
```json
{
  "msg": "ok",
  "status": true
}
```

#### Stat bill order for each #Bill 
* all records were kept in db

**Request**
* Endpoint: `POST /v1/billorder/stat`
* Header:
    - Content-Type: application/json

| Parameter | Type | Required | Example |
|:---------:|:----:|:----------------:|:-------:|
| `bill_no` | str | N | see below |

**Example**
```shell
# query w/ billno
curl -v -X GET 'http://localhost/v1/billorder/stat?billno=1'
# query all (may take longer if the data is big)
curl -v -X GET 'http://localhost/v1/billorder/stat'
```
```json
{
  "data": [
    {
      "bill_no": 1,
      "data": {
        "Hawaiian Pizza": {
          "price": 600,
          "quantity": 2
        },
        "Kimchi": {
          "price": 200,
          "quantity": 4
        },
        "total_price": 800
      }
    }
  ],
  "msg": "ok",
  "status": true
}
```