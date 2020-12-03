## Semantive Task

To build Docker Image run:
```
docker build -t app .
```
To run Docker Image without DB (sqlite:///:memory:)
```
docker run -p 8080:8080 -e BUILD_ENV='test' app
```
To run Docker Image with DB add DATABASE_URL='mysql+pymysql://user:pass@host:port/dbname' and set BUILD_ENV as production or development
```
docker run -p 8080:8080 -e BUILD_ENV='production' -e DATABASE_URL='mysql+pymysql://user:pass@host:port/dbname' app
```
## API requests for Images:
Save All images to DB:
```
POST http://127.0.0.1:8080/semantive/img
```
with body:
```
{
    "name": "task1",
    "url": "https://semantive.com"
}
```
Download encoded Image via GET\id (id taken from POST response body)
```
GET http://127.0.0.1:8080/semantive/img/138263036848061130
```
Download all decoded images from DB
```
GET http://127.0.0.1:8080/semantive/img
```
Delete Image from DB:
```
DELETE http://127.0.0.1:8080/semantive/img/138263036848061130
```
## API requests for Text:
Save all Text from webside to DB:
```
POST http://127.0.0.1:8080/semantive/txt
```
with body:
```
{
    "name": "task2",
    "url": "https://semantive.com"
}
```
Download Text via GET\id (id taken from POST response body)
```
GET http://127.0.0.1:8080/semantive/txt/1
```
Download all saved texts from DB
```
GET http://127.0.0.1:8080/semantive/txt
```
Update Text via PUT\id (id taken from POST response body)
```
PUT http://127.0.0.1:8080/semantive/txt/1
```
with body:
```
{
    "name": "update task2",
    "url": "https://semantive.com"
}
```
Delete Text from DB:
```
DELETE http://127.0.0.1:8080/semantive/txt/1
```

