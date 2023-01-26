# http-monitor

An HTTP endpoint monitor service written in go with RESTful API.

## Run

- You can run the project using docker-compose by running `docker-compose up` ( change container port in `docker-compose.yml`)

## Database

### Tables : 

#### **Users:**

| id(pk)  | created_at |   username   |   password   |
| :------ | ---------- | ------------ | ------------ |
| integer | datetime   | varchar(255) | varchar(255) |

#### **URLs:**

| id(pk)  | created_at | user_id(fk) |     url      |    method   |   threshold  |
| :------ | ---------- | ----------  |  ----------  | ----------- | ------------ |
| integer | datetime   | varchar(255)| varchar(255) | varchar(255)|    integer   |

#### **Requests:**

| id(pk)  | created_at | url_id(fk) | status_code  |
| ------- | ---------- | ---------- | -----------  |
| integer | datetime   | integer    |    integer   |

#### **Alerts:**

| id(pk)  | created_at | url_id(fk  |
| ------- | ---------- | ---------  |
| integer | datetime   | integer    |

## API

### Specs:

For all requests and responses we have `Content-Type: application/json`.

Authorization is with JWT.

### User endpoints:

#### **Login:**

`POST /api/users/login`

request structure: 

```
{
	"username":"foo", // alpha numeric, length >= 4
	"password":"*bar*" // text, length >=4 
}
```

#### **Sign Up:**

`POST /api/users`

request structure (same as login):

```
{
	"username":"foo", // alpha numeric, length >= 4
	"password":"*bar*" // text, length >=4 
}
```

### URL endpoints:

#### **Create URL:**

`POST /api/urls`

request structure:

```
{
	"url":"http://some-valid-url.com" // valid url address
	"method":"GET" // valid url method
	"threshold":20 // url fail threshold
}
```

#### **Get user URLs:**

`GET /api/urls`

####**Get URL stats:**

`GET /api/urls/:urlID`

`urlID` a valid url id

#### **Get URL alerts:**

`GET /api/alerts`
