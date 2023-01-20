# http-monitor

A HTTP endpoint monitor service written in go with RESTful API.

## Run

- You can run the project using docker-compose by running `docker-compose up` ( change container port in `docker-compose.yml`)

## Database

#### Tables : 

**Users:**

| id(pk)  | created_at |   username   |   password   |
| :------ | ---------- | ------------ | ------------ |
| integer | datetime   | varchar(255) | varchar(255) |

**URLs:**

| id(pk)  | created_at | user_id(fk) |   address    |    method   |   threshold  | failed_times |
| :------ | ---------- | ----------  |  ----------  | ----------- | ------------ | ------------ |
| integer | datetime   | varchar(255)| varchar(255) | varchar(255)|    integer   |    integer   |

**Requests:**

| id(pk)  | created_at | url_id(fk) | result  |
| ------- | ---------- | ---------- | ------- |
| integer | datetime   | integer    | integer |

## API

### Specs:

For all requests and responses we have `Content-Type: application/json`.

Authorization is with JWT.

#### User endpoints:

**Login:**

`POST /api/users/login`

request structure: 

```
{
	"username":"foo", // alpha numeric, length >= 4
	"password":"*bar*" // text, length >=4 
}
```

**Sign Up:**

`POST /api/users`

request structure (same as login):

```
{
	"username":"foo", // alpha numeric, length >= 4
	"password":"*bar*" // text, length >=4 
}
```

#### URL endpoints:

**Create URL:**

`POST /api/urls`

request structure:

```
{
	"address":"http://some-valid-url.com" // valid url address
	"threshold":20 // url fail threshold
}
```

##### **Get user URLs:**

`GET /api/urls`

**Get URL stats:**

`GET /api/urls/:urlID`

`urlID` a valid url id

**Get URL alerts:**

`GET /api/alerts`

#### Responses:

##### Errors:

If there was an error during processing the request, a json response with the following format is returned with related response code: 

```
{
	"errors":{
		"key":"value" // a list of key,value of errors occurred
	}
}
```

##### URL stat:

```
{
    "data": {
        "url": "http://google.com",
        "requests_count": 1,
        "requests": [
            {
                "result_code": 200,
                "created_at": "2019-01-16T14:07:25.443300581+03:30"
            }
        ]
    }
}
```

##### List of URLs:

```
{
    "data": {
    	"url_count": 1,
        "urls": [
            {
                "id": 0,
                "url": "http://google.com",
                "user_id": 1,
                "created_at": "2020-01-16T14:07:15.066047519+03:30",
                "threshold": 10,
                "failed_times": 0
            }
        ]
    }
}
```

##### Request report:

```
{
	"data": "A message with report"
}
```
