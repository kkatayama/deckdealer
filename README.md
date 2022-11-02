# [Web Framework](#Web-Framework)
[https://deckdealer.hopto.org](https://deckdealer.hopto.org)

Framework is loosely modeled after CRUD: [C]reate [R]ead [U]pdate [D]elete

**Features:**
* [*User Functions*](#User-Functions) &nbsp;&nbsp; - [**`/login`**](#1-login), [**`/logout`**](#2-logout), [**`/register`**](#3-register)
* [*Admin Functions*](#Admin-Functions)            - [**`/createTable`**](#1-createTable), [**`/deleteTable`**](#2-deleteTable)
* [*Core Functions*](#Core-Functions) &nbsp;&nbsp; - [**`/add`**](#1-add), [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete)
* [*Extra_Functions*](#Extra-Functions) &nbsp;     - [**`/uploadImageUrl`**](#1-uploadImageUrl)
* Query and URL path parameter support
* Additional [**`filter`**](#notes-on-filter-option) parameter - enables SQLite expressions containing operators 
* In-place column editing with SQLite3 expression support
* [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete) supports single and multiple simultaneous table transactions
* Changes made to the **backend.db** database are now automatically updated to the GitHub repo in *real-time*

**Design Constrains:**
* All  **`table_names`** and **`column_names`** are defined with **lowercase** letters
* A column name with suffix **`_id`** reference a **unique item** or a **unique item group**.
* A column name with suffix **`_time`** reference a **unique datetime item**
* All tables must have a **`{ref}_id`** `column` to be used as `PRIMARY KEY`
* All tables must have a **`{ref}_time`** `column` 

**4 User Functions:**
1. [**`/login`**](#1-login) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Login a user
2. [**`/logout`**](#2-logout) &nbsp;&nbsp;&nbsp; - Logout a user
3. [**`/register`**](#3-register) - Register a new user
4. [**`/status`**](#4-status) &nbsp;&nbsp;&nbsp; - Verify signed session cookies

**2 Admin Functions**
1. [**`/createTable`**](#1-createTable) - Create a new `table` 
2. [**`/deleteTable`**](#2-deleteTable) - Delete an existing `table`

**4 Core Functions:**
1. [**`/add`**](#1-add) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Add a *single* entry to a `table`
2. [**`/get`**](#2-get) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Fetch a *single* entry or *multiple* entries from a `table`
3. [**`/edit`**](#3-edit) &nbsp;&nbsp;&nbsp; - Edit a *single* entry or *multiple* entries in a `table`
4. [**`/delete`**](#4-delete) - Delete a *single* entry or *multiple* entries from a `table`

**1 Extra Function**
1. [**`uploadImageUrl`**](#1-uploadImageUrl) - Upload an image to the backend via `image_url`

---

<details><summary>Debugging Tip! (click me to expand)</summary>
<p>

To see all of the available `tables` along with the `column_names` and the `column_types`, make a request to the root path of any `core` or `admin` function:

Request:
```ruby
https://deckdealer.hopto.org/add
https://deckdealer.hopto.org/get
https://deckdealer.hopto.org/edit
https://deckdealer.hopto.org/delete
https://deckdealer.hopto.org/createTable
https://deckdealer.hopto.org/deleteTable
```

Response:
```json
{ "message": "active tables in the database",
  "tables": [
    { "name": "users",
      "type": "table",
      "columns": [
        { "name": "user_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "username", "type": "TEXT NOT NULL" },
        { "name": "password", "type": "TEXT NOT NULL" },
        { "name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    },
    { "name": "oximeter", 
      "type": "table",
      "columns": [
        { "name": "entry_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "user_id", "type": "INTEGER NOT NULL" },
        { "name": "heart_rate", "type": "INTEGER NOT NULL" },
        { "name": "blood_o2", "type": "INTEGER NOT NULL" },
        { "name": "temperature", "type": "DOUBLE NOT NULL" },
        { "name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    }
  ]
}
```

If you receive an `invalid token` response, then the request you are making does not contain the `session cookie`. <br />
**REQUESTS TO `/login` SHOULD BE DONE AS A `POST` REQUEST** <br />
The `session cookie` is assigned after a successful login. <br />
To get around adding the `session cookie` along with your request, you can simply add the `token` parameter. <br />

PLEASE LET ME KNOW IF YOU WISH TO DISABLE THE SESSION COOKIES AND TOKENS!!! <br />

FOR EXAMPLE:

### You logged in with the `admin` user doing a `GET` request:
Request:
```ruby
/login?username=admin&password=admin
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```

### But all of the requests return `invalid token`...?
Request:
```ruby
/add
```

Response:
```json
{
  "message": "invalid token"
}
```

### Simply append the token parameter to all requests
Request:
```ruby
/add?token=IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09
```

Response:
```json
{ "message": "active tables in the database",
  "tables": [
    { "name": "users",
      "type": "table",
      "columns": [
        { "name": "user_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "username", "type": "TEXT NOT NULL" },
        { "name": "password", "type": "TEXT NOT NULL" },
        { "name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    },
    { "name": "oximeter", 
      "type": "table",
      "columns": [
        { "name": "entry_id", "type": "INTEGER PRIMARY KEY" },
        { "name": "user_id", "type": "INTEGER NOT NULL" },
        { "name": "heart_rate", "type": "INTEGER NOT NULL" },
        { "name": "blood_o2", "type": "INTEGER NOT NULL" },
        { "name": "temperature", "type": "DOUBLE NOT NULL" },
        { "name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))" }
      ]
    }
  ]
}
```

### When using `curl`, add `-b` and `-c` to save and read session cookies
``` ruby
curl -XPOST -b cookie.txt -c cookie.txt 'http://deckdealer.hopto.org/login' -d '{"username": "admin", "password": "admin"}'
curl -b cookie.txt -c cookie.txt 'http://deckdealer.hopto.org/get/users'
```
</p>
</details>

---

# [Getting Started](#Getting-Started)
Follow the [Setup Guide](SERVER_SETUP.md) to install and configure the framework. <br />

You can choose to run the server locally or connect with the server all ready running at: <br />
[https://deckdealer.hopto.org](https://deckdealer.hopto.org)

To interact with the framework (locally or remote) you will need to first login. <br />

I recommend starting with the [Workflows](#Workflows) provided to get comfortable with using this framework. <br />

## [Workflows](#Workflows):
- [ ] [Workflow 1 - Login](#Workflow-1---Login)
- [ ] [Workflow 2 - Register Users](#Workflow-2---Register-Users)
- [ ] [Workflow 3 - Creating Tables](#Workflow-3---Creating-Tables)
- [ ] [Workflow 4 - Inserting Data](#Workflow-4---Inserting-Data)
- [ ] [Workflow 5 - Requesting Data](#Workflow-5---Requesting-Data)
- [ ] [Workflow 6 - Editing Data](#Workflow-6---Editing-Data)
- [ ] [Workflow 7 - Deleting Data](#Workflow-7---Deleting-Data)

---

# [User Functions](#User-Functions)
The examples listed below will cover the **4 user functions**.<br />
All examples were executed with a **GET** request and can be tested in any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

## 1. `/login`
**Login `user`** 
> NOTE: Only logged in users can call functions!
> NOTE: This request shold be a `POST` request.  Even though you can make a `GET` request, doing so may not store your `session cookie`! 

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/login
```
</td><td>

```rexx
return: {"message": "missing parameters"}
```
</td></tr><tr></tr><tr><td>

```jq
/login/<param_name>/<param_value>
```
</td><td>

```rexx
login with url_paths: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/login/param_name=param_value
```
</td><td>

```rexx
login with params: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
username
```
</td><td>

```rexx
must match the users table
```
</td></tr><tr></tr><tr><td>

```rexx
password
```
</td><td>

```rexx
passwords are salted and pbkdf2 hmac sha256 hashed with 1000 iterations
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/login`
Request:
```ruby
/login
```

Response:
```json
{
  "message": "missing parameters", 
  "required": [{"username": "TEXT", "password": "TEXT"}], "submitted": [{}]
}
```

Arguments:
```python
username = admin
```

Request:
```ruby
/login/username/admin
```

Response:
```json
{
  "message": "missing parameters",
  "required": [{"username": "TEXT", "password": "TEXT"}],
  "submitted": [{"username": "admin"}]
}
```

Arguments:
```python
username = admin
password = 123
```

Request:
```ruby
/login?username=admin&password=123
```

Response:
```json
{
  "message": "incorrect password",
  "password": "123"
}
```

Arguments:
```python
username = admin
password = admin
```

Request:
```ruby
/login?username=admin&password=admin
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```
</details>

---

## [Workflow 1 - Login](#Workflow-1---Login)

<details><summary> (click here to expand) </summary>

### Let's log in as the user `admin`
Arguments:
```python
username = admin
password = admin
```

POST Request:
```ruby
POST(url='https://deckdealer.hopto.org/login', data={"username": "admin", "password": "admin"})
```

Response:
```json
{
  "message": "user login success",
  "user_id": 1,
  "username": "admin",
  "token": "ITVIMUxRUitCTjdwYUwxbjdESWh3MHc9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
}
```

> Note: the `token` is only needed when api requests do not store session cookies.

### Verify session by making a request to `/status`
Request:
```jq
https://deckdealer.hopto.org/status
```

Response:
```json

{
  "message": "user is logged in with valid session cookie",
  "user_id": "1",
  "cookies": {
    "user_id": "!5H1LQR+BN7paL1n7DIhw0w==?gAWVEQAAAAAAAACMB3VzZXJfaWSUjAExlIaULg=="
  }
}
```

</details>

---

## 2. `/logout`
Terminate a logged in session

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/logout
```
</td><td>

```rexx
delete the user's signed cookie session token
```
</td></tr>
</table>

### Response After Successful [`/logout`](#2-logout)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'user logged out'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
the user_id that was affiliated with the signed cookie session token 
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)
</summary>

### Investigating the Endpoint `/logout`
Request:
```ruby
/logout
```

Response:
```json
{
  "message": "user logged out",
  "user_id": "1"
}
```

</details>

---

## 3. `/register`
Register a new **`user`** to the `users` table.

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/register
```
</td><td>

```rexx
returns: {"message": "missing parameters", "required params": ["username", "password", "password2"]}
```
</td></tr><tr></tr><tr><td>

```jq
/register/usage
```
</td><td>

```rexx
returns: {"message": "usage_info"}
```
</td></tr><tr></tr><tr><td>

```jq
/register/<param_name>/<param_value>
```
</td><td>

```rexx
register with url_paths: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/register?param_name=param_value
```
</td><td>

```rexx
register with params: 'param_name=param_value'
```
</td></tr>
</table>

### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
username
```
</td><td>

```rexx
must be unique (not exist in users table)
```
</td></tr><tr></tr><tr><td>

```rexx
password
```
</td><td>

```rexx
must match password2
```
</td></tr><tr></tr><tr><td>

```rexx
password2
```
</td><td>

```rexx
must match password
```
</td></tr>
</table>


### Response After Successful [`/register`](#3-register)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'new user created'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
the {ref}_id for the user generated by PRIMARY_KEY of the users table
```
</td></tr><tr></tr><tr><td>

```rexx
username 
```
</td><td>

```rexx
user supplied paramater
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint `/register`
Request:
```ruby
/register
```

Response:
```json
{"message": "missing parameter", "required params": ["username", "password", "password2"]}
```

---

Request:
```ruby
/register/usage
```

Response:
```json
{
    "message": "usage info: /register",
    "description": "Register a new user to the [users] table",
    "end_points": {
        "/register": {"returns": "missing paramaters"},
        "/register/<param_name>/<param_value>": {
            "url_paths": "register with: \"param_name=param_value\"",
            "example": "/register/username/admin/password/admin",
            "response": {"message": "new user created", "user_id": 2, "username": "teddy"}
        },
        "/register?param_name=param_value": {
            "url_paths": "register with: \"param_name=param_value\"",
            "example": "/register?username=teddy&password=teddy&password2=teddy",
            "response": {"message": "new user created", "user_id": 2, "username": "teddy"}
        },
        "Required": {"Parameters": {"username": "TEXT", "password": "TEXT", "password2": "TEXT"}},
        "Response": {"message": "new user created", "user_id": "INTEGER", "username": "TEXT", "token": "TEXT"}
    }
}
```

---

Request:
```ruby
/register/username/teddy/password/teddy/password2/ted
```

Response:
```json
{"message": "passwords do not match", "password1": "teddy", "password2": "ted"}
```

---

Request:
```ruby
/register/username/teddy/password/teddy/password2/teddy
```

Response:
```json
{"message": "new user created", "user_id": 2, "username": "teddy"}
```

---

Request:
```ruby
/register?username=teddy&password=teddy&password2=teddy
```

Response:
```json
{"message": "user exists", "username": "teddy"}
```

</details>

---

## [Workflow 2 - Register Users](#Workflow-2---Register-Users)

<details><summary> (click here to expand) </summary>

### Let's create a few users by registering them: `alice`, `bob`, `anna`, `steve`, `ellan`, `jimmy`
---

Arguments:
```rexx
username = alice
password = alice
password2 = alice
```

Request:
```jq
https://deckdealer.hopto.org/register/username/alice/password/alice/password2/alice
```

Response:
```json
{"message": "new user created", "user_id": 2, "username": "alice"}
```
---

Arguments:
```rexx
username = bob
password = bob
password2 = bob
```

Request:
```jq
https://deckdealer.hopto.org/register/username/bob/password/bob/password2/bob
```

Response:
```json
{"message": "new user created", "user_id": 3, "username": "bob"}
```
---

Arguments:
```rexx
username = anna
password = anna
password2 = anna
```

Request:
```jq
https://deckdealer.hopto.org/register/username/anna/password/anna/password2/anna
```

Response:
```json
{"message": "new user created", "user_id": 4, "username": "anna"}
```
---

Arguments:
```rexx
username = steve
password = steve
password2 = steve
```

Request:
```jq
https://deckdealer.hopto.org/register/username/steve/password/steve/password2/steve
```

Response:
```json

{
  "message": "new user created",
  "user_id": 5,
  "username": "steve"
}
```

</details>

---

## 4. `/status`
Verify signed cookie sessions

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/status
```
</td><td>

```rexx
Verify the session cookie is signed with a valid token
```
</td></tr>
</table>

### Response After Successful [`/status`](#2-logout)
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
'user is logged in with valid session cookie'
```
</td></tr><tr></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
'the user_id of the logged in user with a signed cookie session token' 
```
</td></tr><tr></tr><tr><td>

```rexx
cookies
```
</td><td>

```rexx
'the session token'
```
</td><td>
</table>

---

# [Admin Functions](#Admin-Functions)
The examples listed below will cover the **2 admin functions**. <br />
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4  *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

## 1. `/createTable`
**Create a new `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/createTable
```
</td><td>

```rexx
returns a list of all existing tables in the database
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/{table_name}
```
</td><td>

```rexx
debug: returns the required parameters
```
</td></tr><tr></tr><tr><td>

```jq
/createTable/{table_name}/{column_name}/{column_type}
```
</td><td>

```rexx
create a table with columns using path parameters
```
</td></tr><tr></tr><tr><td>

```erlang
/createTable/{table_name}?column_name=column_type
```
</td><td>

```rexx
create a table with columns using query parameters
```
</td></tr>
</table>

### Requirements:
<table>
</td></tr><tr><td> Parameters </td><td> Value </td></tr><tr><td>

```rexx
{ref}_id
```
</td><td>

```rexx
INTEGER - to be used as the PRIMARY_KEY for the table where the ID is automatically created
```
</td></tr><tr></tr><tr><td>

```rexx
{ref}_time
```
</td><td>

```rexx
DATETIME - autogenerated date-timestamp assigned with every table entry transaction 
```
</td></tr><tr></tr><tr><td>

```rexx
column_name 
```
</td><td>

```rexx
categorical reference to data - should only consist of underscore and lowercase letters 
```
</td></tr><tr></tr><tr><td>

```rexx
column_type
```
</td><td>

```rexx
currently impleted data types: INTEGER, DOUBLE, TEXT, DATETIME
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/createTable`
The endpoint for creating a **`table`** with a **`table_name`** is **`/createTable/{table_name}`**. <br />
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/createTable/steps
```

Response:
```json
{
    "message": "missing paramaters",
    "required": [
        {
            "user_id": "INTEGER",
            "{ref}_id": "INTEGER",
            "{ref}_time": "DATETIME",
            "column_name": "column_type",
            "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"]
        }
    ],
    "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"],
    "Exception": "\"{ref}_id\" not required when creating \"users\" table",
    "submitted": []
}
```

### Creating the Table `steps`
Arguments:
```python
step_id    = INTEGER
user_id    = INTEGER
step_count = INTEGER
latitude   = DOUBLE
longitude  = DOUBLE
step_time  = DATETIME
```

Request:
```ruby
/createTable/steps/step_id/INTEGER/user_id/INTEGER/step_count/INTEGER/latitude/DOUBLE/longitude/DOUBLE/step_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "steps",
    "columns": [
        "step_id INTEGER PRIMARY KEY",
        "user_id INTEGER NOT NULL",
        "step_count INTEGER NOT NULL",
        "latitude DOUBLE NOT NULL",
        "longitude DOUBLE NOT NULL",
        "step_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `oximeter`
Arguments:
```python
entry_id    = INTEGER
user_id     = INTEGER
heart_rate  = INTEGER
blood_o2    = INTEGER
temperature = DOUBLE
entry_time  = DATETIME
```

Request:
```ruby
/createTable/oximeter/entry_id/INTEGER/user_id/INTEGER/heart_rate/INTEGER/blood_o2/INTEGER/temperature/DOUBLE/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "oximeter",
    "columns": [
        "entry_id    INTEGER PRIMARY KEY",
        "user_id     INTEGER NOT NULL",
        "heart_rate  INTEGER NOT NULL",
        "blood_o2    INTEGER NOT NULL",
        "temperature DOUBLE NOT NULL",
        "entry_time  DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```



</details>

---

## [Workflow 3 - Creating Tables](#Workflow-3---Creating-Tables)

<details><summary> (click here to expand) </summary>

### Existing tables!
<table>
<tr><td> Table Name </td><td> Table Description </td><td> Column Names </td></tr><tr><td>

```rexx
users
```
</td><td>

```css
all registered users
```
</td><td>


```jq
["user_id", "username", "password", "create_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
cards
```
</td><td>

```css
all 52 cards in a deck
```
</td><td>


```jq
["card_id", "key", "name", "suit", "description", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
deck
```
</td><td>

```css
52 shuffeled cards (for testing)
```
</td><td>


```jq
["card_id", "key", "name", "suit", "description", "entry_time"]
```
</td></tr>
</table>

The `cards` and `deck` tables have been created for **convenience**. <br />
It contains all `52` cards in a standard `deck`. <br />
In [Workflow 5 - Requesting Data](#Workflow-5---Requesting-Data) you will learn the `/get/<table_name>/<param_key>/<param_value>` endpoint. <br />
Making a request to `/get/cards/name/ACE` will return with all of the `ACE` cards:

Arguments:
```rexx
name = ACE
```

Request:
```jq
https://deckdealer.hopto.org/get/cards/name/ACE
```

Response:
```json
{
  "message": "found 4 card entries",
  "data": [
    {"card_id": 49, "key": "AC", "name": "ACE", "suit": "CLUBS", "description": "ace_of_clubs", "file_name": "AC.png", "entry_time": "2022-11-01 13:05:10.839"},
    {"card_id": 50, "key": "AD", "name": "ACE", "suit": "DIAMONDS", "description": "ace_of_diamonds", "file_name": "AD.png", "entry_time": "2022-11-01 13:05:11.490"},
    {"card_id": 51, "key": "AH", "name": "ACE", "suit": "HEARTS", "description": "ace_of_hearts", "file_name": "AH.png", "entry_time": "2022-11-01 13:05:12.118"},
    {"card_id": 52, "key": "AS", "name": "ACE", "suit": "SPADES", "description": "ace_of_spades", "file_name": "AS.png", "entry_time": "2022-11-01 13:05:12.745"},
  ],
}
```

To view the pictures for each card, make a request to `/<file_name>` <br />
| https://deckdealer.hopto.org/AC.png  | https://deckdealer.hopto.org/AD.png  | https://deckdealer.hopto.org/AH.png  | https://deckdealer.hopto.org/AS.png  |
|:-:|:-:|:-:|:-:|
| ![AC.png](https://deckdealer.hopto.org/AC.png) | ![AD.png](https://deckdealer.hopto.org/AD.png) | ![AH.png](https://deckdealer.hopto.org/AH.png) | ![AS.png](https://deckdealer.hopto.org/AS.png) |


### Let's create a few tables!<br />
<table>
<tr><td> Table Name </td><td> Table Description </td><td> Column Names </td></tr><tr><td>

```rexx
players
```
</td><td>

```css
users playing an active game
```
</td><td>

```jq
["player_id", "user_id", "game_id", "name", "email", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
spectators
```
</td><td>

```css
users watching an active game
```
</td><td>

```jq
["spectator_id", "user_id", "game_id", "name", "email", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
games
```
</td><td>

```css
game config and card values
```
</td><td>

```jq
["game_id", "name", "min_players", "max_players", "min_decks", "max_decks", "player_actions", "rules", "entry_time"]
```
</td></tr><tr></tr><tr><td>


```rexx
active_game
```
</td><td>

```css
log for game in play
```
</td><td>

```jq
["entry_id", "game_id", "user_id", "player_id", "player_hand", "player_action", "entry_time"]
```
</td></tr><tr></tr><tr><td>


```rexx
score_board
```
</td><td>

```css
score for completed games
```
</td><td>

```jq
["score_id", "game_id", "user_id", "player_id", "winner", "winner_hand", "winner_score", "players", "player_hands", "player_scores", "spectators", "entry_time"]
```
</td></tr>
</table>

---

### Creating the Table `players`:
Request:
```jq
https://deckdealer.hopto.org/createTable/players/player_id/INTEGER/user_id/INTEGER/game_id/INTEGER/name/TEXT/email/TEXT/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "players",
  "columns": [
    "player_id INTEGER PRIMARY KEY",
    "user_id INTEGER NOT NULL",
    "game_id INTEGER NOT NULL",
    "name TEXT NOT NULL",
    "email TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
  ]
}
```

### Creating the Table `spectators`:
Request:
```jq
https://deckdealer.hopto.org/createTable/spectators/spectator_id/INTEGER/user_id/INTEGER/game_id/INTEGER/name/TEXT/email/TEXT/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "spectators",
  "columns": [
    "spectator_id INTEGER PRIMARY KEY",
    "user_id INTEGER NOT NULL",
    "game_id INTEGER NOT NULL",
    "name TEXT NOT NULL",
    "email TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
  ]
}
```

### Creating the Table `games`:
Request:
```jq
https://deckdealer.hopto.org/createTable/games/game_id/INTEGER/name/TEXT/min_players/TEXT/max_players/TEXT/min_decks/TEXT/max_decks/TEXT/player_actions/TEXT/rules/TEXT/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "games",
  "columns": [
    "game_id INTEGER PRIMARY KEY",
    "name TEXT NOT NULL",
    "min_players TEXT NOT NULL",
    "max_players TEXT NOT NULL",
    "min_decks TEXT NOT NULL",
    "max_decks TEXT NOT NULL",
    "player_actions TEXT NOT NULL",
    "rules TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
  ]
}
```

### Creating the Table `active_game`:
Request:
```jq
https://deckdealer.hopto.org/createTable/active_game/entry_id/INTEGER/game_id/INTEGER/user_id/INTEGER/player_id/INTEGER/player_hand/TEXT/player_action/TEXT/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "active_game",
  "columns": [
    "entry_id INTEGER PRIMARY KEY",
    "game_id INTEGER NOT NULL",
    "user_id INTEGER NOT NULL",
    "player_id INTEGER NOT NULL",
    "player_hand TEXT NOT NULL",
    "player_action TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
  ]
}
```

### Creting the Table `score_board`:
Request:
```jq
https://deckdealer.hopto.org/createTable/score_board/score_id/INTEGER/game_id/INTEGER/user_id/INTEGER/player_id/INTEGER/winner/TEXT/winner_email/TEXT/winner_hand/TEXT/winner_score/INTEGER/players/TEXT/player_hands/TEXT/player_scores/TEXT/spectators/TEXT/entry_time/DATETIME
```

Response:
```json

{
  "message": "1 table created",
  "table": "score_board",
  "columns": [
    "score_id INTEGER PRIMARY KEY",
    "game_id INTEGER NOT NULL",
    "user_id INTEGER NOT NULL",
    "player_id INTEGER NOT NULL",
    "winner TEXT NOT NULL",
    "winner_email TEXT NOT NULL",
    "winner_hand TEXT NOT NULL",
    "winner_score INTEGER NOT NULL",
    "players TEXT NOT NULL",
    "player_hands TEXT NOT NULL",
    "player_scores TEXT NOT NULL",
    "spectators TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ]
}
```

</details>

---


## 2. `/deleteTable`
**Delete `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/deleteTable
```
</td><td>

```rexx
returns a list of all existing tables in the database
```
</td></tr><tr></tr><tr><td>

```jq
/deleteTable/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/deleteTable/{table_name}
```
</td><td>

```rexx
debug: returns the required parameters
```
</td></tr>
</table>

### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr><tr><td>

```rexx
table_name
```
</td><td>

```rexx
the name of the table you wish to delete
```
</td></tr>
</table>

---

<details>
<summary>Endpoint Background (click here to expand)</summary>



### Investigating the Endpoint: `/deleteTable`
The endpoint for deleting a **`table`** with a **`table_name`** is **`/deleteTable/{table_name}`**.

### Let's Delete the Table `steps`
Request:
```ruby
/deleteTable/steps
```

Response:
```json
{"message": "1 table deleted!", "table": "steps"}
```

Verify the **`steps`**** table no longer exists

Request:
```ruby
/deleteTable
```

Response:
```json
{
    "message": "active tables in the database",
    "tables": [
        {
            "name": "users",
            "type": "table",
            "columns": [
                {"name": "user_id", "type": "INTEGER PRIMARY KEY"},
                {"name": "username", "type": "TEXT NOT NULL"},
                {"name": "password", "type": "TEXT NOT NULL"},
                {"name": "create_time", "type": "DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"}
            ]
        },
        {
            "name": "oximeter",
            "type": "table",
            "columns": [
                {"name": "entry_id", "type": "INTEGER PRIMARY KEY"},
                {"name": "user_id", "type": "INTEGER NOT NULL"},
                {"name": "heart_rate", "type": "INTEGER NOT NULL"},
                {"name": "blood_o2", "type": "INTEGER NOT NULL"},
                {"name": "temperature", "type": "DOUBLE NOT NULL"},
                {"name": "entry_time", "type": "DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"}
            ]
        }
    ]
}
```
</details> 

---

# [Core Functions](#Core-Functions)
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE** <br />

## 1. `/add`
**Add a *single* entry to a `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/add
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/add/usage
```
</td><td>

```rexx
returns message: 'usage info'
```
</td></tr><tr></tr><tr><td>

```jq
/add/{table_name}
```
</td><td>

```rexx
returns message: 'missing parameters'
```
</td></tr><tr></tr><tr><td>

```jq
/add/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
add entry: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/add/{table_name}?param_name=param_value
```
</td><td>

```rexx
add entry: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Exception </td></tr><tr><td>

```rexx
All params not {ref}_id or {ref}_time
```
</td><td>

```rexx
{ref}_id required when not PRIMARY KEY
```
</td></tr>
</table>

### Response After Successful [`/add`](#1-add):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
user_id
```
</td><td>

```rexx
when entry added to users table
```
</td></tr><tr></tr><tr><td>

```rexx
{ref}_id
```
</td><td>

```rexx
when entry added to any other table
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)
</summary>

### Investigating the Endpoint: `/add`
The endpoint for adding a user to the **`users`** table is **`/add/users`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/add/users
```

Response:
```json
{
  "message": "missing parameters", 
  "required": [{"username": "TEXT", "password": "TEXT"}], 
  "missing": [{"username": "TEXT", "password": "TEXT"}], 
  "submitted": [{}]
}
```

Making a request with only 1 of the 2 **required_parameters** updates the `missing parameters` message:

Request:
```ruby
/add/users/username/alice
```

Response:
```json
{
  "message": "missing parameters",
  "required": [{"username": "TEXT", "password": "TEXT"}],
  "missing": [{"password": "TEXT"}],
  "submitted": [{"username": "alice"}]
}
```

### Adding `alice` to the **`users`** table
To add the user `alice`, we need to provide the **username** and **password** parameters
There are several ways to do this: using **url_parameters**, **query_parameters**, or a combination of both.

**Recommended Method: Using URL_Parameters**
```ruby
/add/users/username/alice/password/alice
```
Response:
```json
{
  "message": "data added to {users}",
  "user_id": 7
}
```

*Alternative Methods: Any of these will work but the format may get confusing when using the other **core functions***
```ruby
/add/users?username=alice&password=alice
/add/users/username/alice?password=alice
/add/users/password=alice?username=alice
```

Attempting to add the existing user `alice` will respond with a `user exists` message:

Request
```ruby
/add/users/username/alice/password/alice
```
Response:
```json
{
  "message": "user exists",
  "username": "alice"
}
```

### Adding `bob` to the **`users`** table
Request:
```ruby
/add/users/username/bob/password/bob
```
Response:
```json
{
  "message": "data added to {users}",
  "user_id": 8
}
```

### Adding sensor data for the user `alice` to the **`oximeter`** table
When we added the user `alice` to the **`users`** table, we were provided with the **`user_id = 7`** 
To get the required parameters for adding an `entry` to the **`oximeter`**, make a request without parameters:

Request:
```ruby
/add/oximeter
```

Response:
```json
{
    "message": "missing parameters",
    "required": [{"user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE"}],
    "missing": [{"user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE"}],
    "submitted": [{}]
}
```

Let's add some sensor data for the user `alice` to the **`oximeter`** table by making the following requests:

Request:
```ruby
/add/oximeter/user_id/7/heart_rate/134/blood_o2/97/temperature/97.6691638391727
/add/oximeter/user_id/7/heart_rate/129/blood_o2/98/temperature/97.45331222228752
/add/oximeter/user_id/7/heart_rate/128/blood_o2/100/temperature/97.35755335543793
/add/oximeter/user_id/7/heart_rate/134/blood_o2/96/temperature/97.03691402965539
/add/oximeter/user_id/7/heart_rate/132/blood_o2/96/temperature/97.78609598543946
/add/oximeter/user_id/7/heart_rate/130/blood_o2/98/temperature/97.262831668111
```

Each request had a unique response:
Response:
```json
{"message": "data added to {oximeter}", "entry_id": 43, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 44, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 45, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 46, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 47, "user_id": "7"}
{"message": "data added to {oximeter}", "entry_id": 48, "user_id": "7"}
```

Now let's add some sensor data for the user `bob` to the **`oximeter`** table by making the following requests:

Request:
```ruby
/add/oximeter/user_id/8/heart_rate/143/blood_o2/97/temperature/97.23579109761334
/add/oximeter/user_id/8/heart_rate/127/blood_o2/97/temperature/97.7532770488335
/add/oximeter/user_id/8/heart_rate/131/blood_o2/95/temperature/97.89202180155488
/add/oximeter/user_id/8/heart_rate/124/blood_o2/95/temperature/97.81020200542864
/add/oximeter/user_id/8/heart_rate/133/blood_o2/95/temperature/101.7115308733577
/add/oximeter/user_id/8/heart_rate/133/blood_o2/100/temperature/103.10357503270177
/add/oximeter/user_id/8/heart_rate/144/blood_o2/98/temperature/103.35133621760384
/add/oximeter/user_id/8/heart_rate/134/blood_o2/98/temperature/102.16442367992002
/add/oximeter/user_id/8/heart_rate/132/blood_o2/98/temperature/101.79215076652413
/add/oximeter/user_id/8/heart_rate/130/blood_o2/99/temperature/102.76488036781804
```

Response:
```json
{"message": "data added to {oximeter}", "entry_id": 49, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 50, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 51, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 52, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 53, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 54, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 55, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 56, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 57, "user_id": "8"}
{"message": "data added to {oximeter}", "entry_id": 58, "user_id": "8"}
```

</details>

---

## [Workflow 4 - Inserting Data](#Workflow-Example-4---Inserting-Data)

<details><summary> (click here to expand) </summary>

We would like to add the game `Blackjack` to the `games` table. <br />

### If we try to add anything the `games` table without parameters, we get a `missing parameters` message:
Request:
```jq
https://deckdealer.hopto.org/add/games
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [{"name": "TEXT", "min_players": "TEXT", "max_players": "TEXT", "min_decks": "TEXT", "max_decks": "TEXT", "player_actions": "TEXT", "rules": "TEXT"}],
  "missing": [{"name": "TEXT", "min_players": "TEXT", "max_players": "TEXT", "min_decks": "TEXT", "max_decks": "TEXT", "player_actions": "TEXT", "rules": "TEXT"}],
  "submitted": [{}],
}
```

### Adding the game `Blackjack` to the `games` table:
> This is the simplest form of `Blackjack`
> 1. All players are dealt 2 cards
> 2. Dealer asks each player to "hit" or "stay"
> 3. Dealer hits until hand is at least 17
> 4. Hand that is closest to 21 but not greater WINS
Arguments:
```rexx
name = Blackjack
min_players = 2
max_players = 10
min_decks = 1
max_decks = 10
player_actions = setup, hit, stay
rules = 1. All players are dealt 2 cards, 2. Dealer asks each player to "hit" or "stay", 3. Dealer hits until hand is at least 17, 4. Hand that is closest to 21 but not greater WINS
```

Request:
```jq
https://deckdealer.hopto.org/add/games/name/Blackjack/min_players/2/max_players/10/min_decks/1/max_decks/10/player_actions/setup, hit, stay/rules/1. All players are dealt 2 cards, 2. Dealer asks each player to "hit" or "stay", 3. Dealer hits until hand is at least 17, 4. Hand that is closest to 21 but not greater WINS
```

Response:
```json

{
  "message": "data added to <games>",
  "game_id": 1
}
```

</details>

---

# 2. `/get`
**Fetch a *single* entry or *multiple* entries from a `table`**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/get
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/get/usage
```
</td><td>

```rexx
returns a message for how to use this function
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}
```
</td><td>

```rexx
returns all entries for the table: {table_name}
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
match entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?param_name=param_value
```
</td><td>

```rexx
match entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/filter/{query}
```
</td><td>

```rexx
match entries: 'filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?filter=query
```
</td><td>

```rexx
match entries: 'filter='
```
</td></tr>
</table>


### Options:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
*None*
```
</td><td>

```rexx
submit no parameters (none required)
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/key/value
```
</td><td>

```rexx
match is limited to 'column_name == column_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?key=value
```
</td><td>

```rexx
match is limited to 'column_name == column_value'
```
</td></tr><tr></tr><tr><td>

```jq
/get/{table_name}/filter/query
```
</td><td>

```rexx
supports expressions, operators, and functions
```
</td></tr><tr></tr><tr><td>

```erlang
/get/{table_name}?filter=query
```
</td><td>

```rexx
supports expressions, operators, and functions
```
</td></tr>
</table>

### Notes on `filter` option:
<table>
<tr><td> Note </td><td> Comment </td></tr><tr><td>

```rexx
keyword
```
</td><td>

```rexx
filter
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY FORMAT
```
</td><td>

```erlang
/get/{table_name}?filter=(param_name > "param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY EXAMPLE
```
</td><td>

```erlang
/get/users?filter=(user_id = "7" OR username="bob")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH FORMAT
```
</td><td>

```jq
/get/{table_name}/filter/(param_name="param_value" OR param_name="param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH EXAMPLE
```
</td><td>

```jq
/get/users/filter/(username="bob" OR username="alice")
```
</td></tr>
</table>

### Response After Successful [`/get`](#2-get):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
data = {obj}
```
</td><td>

```rexx
a single object matching the parameters
```
</td></tr><tr></tr><tr><td>

```rexx
data = [{obj}]
```
</td><td>

```rexx
an array of objects matching the parameters
```
</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/get`
The endpoint for getting users from the **`users`** table is **`/get/users`**.


### Let's query the **`users`** table to find the 2 users we created earlier
Examine the **`users`** table
Request:
```ruby
/get/users
```

Response:
```json
{
    "message": "found 8 user entries",
    "data": [
        {"user_id": 1, "username": "user_1", "password": "794001bff7f6ae7ded745c7de77043873b4173fad011d3ee5ba42bea334d99486f38d77f246009a052277d7b56dddd90337d5f18cf7fa065ed287e6b8661a279", "create_time": "2022-04-01 23:09:19.000"},
        {"user_id": 2, "username": "user_2", "password": "828beaa5b092bc374d1a443847ea68f1d83e4991b83c2e95e961ce4817138b7c53c7eb8be731d5bb0c3bfbe7d0335fe3f5ccc1b674d93c89c27d6b644da56875", "create_time": "2022-04-01 23:16:26.000"},
        {"user_id": 3, "username": "user_3", "password": "a3bfdbe9284aecf165cf3fad3ff9c66c3ffa08fe930a2de52094a039062573b00642870e7a304500b1c62a9d0b50d0ffab4a4e08ffc028c86b2f46acae92be74", "create_time": "2022-04-01 23:16:36.000"},
        {"user_id": 4, "username": "user_4", "password": "e820f57e418d387107bfb9e57119e9aa7c3e1db9ef06b1b107c0eb8444b57b69cee1fac48feeb33c7dc34904e0a38e84dd9b6b44fd51078c8359fc272d5af13d", "create_time": "2022-04-01 23:16:41.000"},
        {"user_id": 5, "username": "user_5", "password": "a3cc8fd887edb257f9e630383eb5569d35d2f2600333cd3ff828e5f35edbedbba64bfac5a7da46013a6877934f57d1e3807116205c556aeef83521d6561408fb", "create_time": "2022-04-01 23:16:48.000"},
        {"user_id": 6, "username": "M2band", "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34", "create_time": "2022-04-03 15:29:41.223"},
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

We just want our 2 users **`alice`** and **`bob`**, let's try querying with different parameters

Arguments:
``` python
username = alice
```

Request:
```ruby
/get/users/username/alice
```

Response:
```json
{
  "message": "1 user entry found",
  "data": {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"}
}
```

Arguments:
``` python
username = bob
```

Request:
```ruby
/get/users/username/bob
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
}
```

Arguments:
``` python
user_id = 7
```

Request:
```ruby
/get/users/user_id/7
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"}
}
```

Arguments:
``` python
user_id = 8
```

Request:
```ruby
/get/users/user_id/8
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
}
```

### Let's try out the **`filter`** parameter to get just the users: **`alice`** and **`bob`**

Arguments:
``` python
filter = (user_id = 7 OR user_id = 8)
```

Request:
```ruby
/get/users?filter=(user_id = 7 OR user_id = 8)
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments: "values" wrapped with double quotations 
``` python
filter = (user_id = "7" OR user_id = "8")
```

Request:
```ruby
/get/users?filter=(user_id = "7" OR user_id = "8")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments:
``` python
filter = (user_id > '6' AND user_id < "9")
```

Request:
```ruby
/get/users?filter=(user_id > '6' AND user_id < "9")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```

Arguments:
``` python
filter = (username="bob" OR username="alice")
```

Request:
```ruby
/get/users/filter/(username="bob" OR username="alice")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {"user_id": 7, "username": "alice", "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a", "create_time": "2022-04-05 03:25:57.163"},
        {"user_id": 8, "username": "bob", "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4", "create_time": "2022-04-05 03:41:12.857"}
    ]
}
```
---
### Notes on {filter_string}:
<table>
<tr><td> Note </td><td> Comment </td></tr><tr><td>

```rexx
keyword
```
</td><td>

```rexx
filter
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY FORMAT
```
</td><td>

```erlang
?filter=(param_name > "param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
QUERY EXAMPLE
```
</td><td>

```erlang
/get/users?filter=(user_id = "7" OR username="bob")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH FORMAT
```
</td><td>

```jq
/filter/(param_name="param_value" OR param_name="param_value")
```
</td></tr><tr></tr><tr><td>

```rexx
PATH EXAMPLE
```
</td><td>

```jq
/get/users/filter/(username="bob" OR username="alice")
```
</td></tr></table>

---

### Next, we will query the **`oximeter`** table to retrieve the sensor data for each user: `alice` and `bob`
Oximeter data for just `alice`:

Arguments:
``` python
user_id = 7
```

Request:
```ruby
/get/oximeter/user_id/7
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 97.6691638391727, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 97.45331222228752, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 97.35755335543793, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 97.03691402965539, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 97.78609598543946, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 97.262831668111, "entry_time": "2022-04-05 12:06:02.669"}
    ]
}
```

Oximeter data for just `bob`:

Arguments:
``` python
user_id = 8
```

Request:
```ruby
/get/oximeter/user_id/8
```

Response:
```json
{
    "message": "found 10 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"}
    ]
}
```

Oximeter data for users with (**`user_id`** BETWEEN "6" AND "9")

Arguments:
``` python
filter = (user_id BETWEEN "6" AND "9")
```

Request:
```ruby
/get/oximeter/filter/(user_id BETWEEN "6" AND "9")
```

Response:
```json
{
    "message": "found 16 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 97.6691638391727, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 97.45331222228752, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 97.35755335543793, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 97.03691402965539, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 97.78609598543946, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 97.262831668111, "entry_time": "2022-04-05 12:06:02.669"},
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"}
    ]
}
```

### Test Case: Fever?
Now let's determine who may have been suspected for having a fever.
Using this definition: *Anything above 100.4 F is considered a fever.*

Arguments:
``` python
filter = (temperature > "100.4") GROUP BY user_id
```

Request:
```ruby
/get/oximeter/filter/(temperature > "100.4") GROUP BY user_id
```

Response:
```json
{
    "message": "1 oximeter entry found",
    "data": {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
}
```

Only **`bob`** reached temperatures above `100.4 F`

### Test Case: MIN, MAX, Temperature Range?
Let's get the range of temperatures from **MIN** to **MAX**

Arguments:
``` python
filter = (user_id = "8") ORDER BY temperature
```

Request:
```ruby
/get/oximeter/filter/(user_id = "8") ORDER BY temperature
```

Response:
```json
{
    "message": "found 10 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}
    ]
}
```

Get **`temperature`** Range of fever

Arguments:
``` python
filter = (temperature > "100.4") ORDER BY temperature
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}
    ]
}
```


Get entry with **MIN** **`temperature`** 

Arguments:
``` python
filter = (temperature > "100.4") ORDER BY temperature LIMIT 1
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature LIMIT 1
```

Response:
```json
{
    "message": "1 oximeter entry found",
    "data": {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
}
```

Get entry with **MAX** **`temperature`** 

Arguments:
``` python
user_id = 8
filter = (temperature > "100.4") ORDER BY temperature DESC
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature DESC
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"},
        {"entry_id": 54, "user_id": 8, "heart_rate": 133, "blood_o2": 100, "temperature": 103.10357503270177, "entry_time": "2022-04-05 12:16:54.808"},
        {"entry_id": 58, "user_id": 8, "heart_rate": 130, "blood_o2": 99, "temperature": 102.76488036781804, "entry_time": "2022-04-05 12:16:55.351"},
        {"entry_id": 56, "user_id": 8, "heart_rate": 134, "blood_o2": 98, "temperature": 102.16442367992002, "entry_time": "2022-04-05 12:16:55.068"},
        {"entry_id": 57, "user_id": 8, "heart_rate": 132, "blood_o2": 98, "temperature": 101.79215076652413, "entry_time": "2022-04-05 12:16:55.213"},
        {"entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.7115308733577, "entry_time": "2022-04-05 12:16:54.651"}
    ]
}
```

Get **MAX**

Arguments:
``` python
user_id = 8
filter = (temperature > "100.4") ORDER BY temperature DESC LIMIT 1
```

Request:
```ruby
/get/oximeter/user_id/8/filter/(temperature > "100.4") ORDER BY temperature DESC LIMIT 1
```

Response
```json
{"message": "1 oximeter entry found", "data": {"entry_id": 55, "user_id": 8, "heart_rate": 144, "blood_o2": 98, "temperature": 103.35133621760384, "entry_time": "2022-04-05 12:16:54.931"}}
```

### Test Case: Filter users created after a start date but before an end date.

Finding users created after `2022-04-02`
> Note: If you only provide a date but do not specify a time, then time 00:00:00 is assumed.

Arguments:
```python
filter = (create_time > "2022-04-03")
```

Request:
```ruby
/get/users?filter=(create_time > "2022-04-03")
```

Response:
```json
{
    "message": "found 3 user entries",
    "data": [
        {
            "user_id": 6,
            "username": "M2band",
            "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34",
            "create_time": "2022-04-03 15:29:41.223"
        },
        {
            "user_id": 7,
            "username": "alice@udel.edu",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        },
        {
            "user_id": 8,
            "username": "robert@udel.edu",
            "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
            "create_time": "2022-04-05 03:41:12.857"
        }
    ]
}
```

Finding users created after `2022-04-03` and before `2022-04-05 03:40:00`

Arguments:
```python
filter = (create_time > "2022-04-03" AND create_time < "2022-04-05 03:40:00")
```

Request:
```ruby
/get/users?filter=(create_time > "2022-04-03" AND create_time < "2022-04-05 03:40:00")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {
            "user_id": 6,
            "username": "M2band",
            "password": "30823caee74ca49fd5699c8de172b515f7a00ab04a04d0641107677af5f372c169746ccdf08b3ba1542c0626d73cb5ebcfec762016cab411e06596e4d2211b34",
            "create_time": "2022-04-03 15:29:41.223"
        },
        {
            "user_id": 7,
            "username": "alice@udel.edu",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        }
    ]
}
```
</details>

---

## [Workflow 5 - Requesting Data](#Workflow-5---Requesting-Data)

---

<details><summary> (click here to expand) </summary>

### Let's simulate playing a full game of `Blackjack`
1. Fetch the rules for the game `Blackjack` from the `games` table 
2. Fetch all registered `users` 
3. Adding `dealer`, `alice` and `bob` to the `players` table
4. Adding `anna` and `steve` to the `spectators` table
5. Simulate the first round of play by dealing 2 cards to each user
6. Simulate each player performing a `player_action` of `hit` or `stay`
7. Determine the winner and add the results to the `score_board` table

---

### 5.1 - Fetch the rules for the game `Blackjack` from the `games` table

<details><summary> (click here to expand) </summary>

There are several ways to do this. <br>

#### We could fetch the game with the `name=Blackjack` from the `games` table:
Arguments:
```rexx
name = Blackjack
```

Request:
```jq
https://deckdealer.hopto.org/get/games/name/Blackjack
```

Response:
```json

{
  "message": "1 game entry found",
  "data": {
    "game_id": 1,
    "name": "Blackjack",
    "min_players": "2",
    "max_players": "10",
    "min_decks": "1",
    "max_decks": "10",
    "player_actions": "setup, hit, stay",
    "rules": "1. All players are dealt 2 cards, 2. Dealer asks each player to \"hit\" or \"stay\", 3. Dealer hits until hand is at least 17, 4. Hand that is closest to 21 but not greater WINS",
    "entry_time": "2022-11-01 21:10:51.915"
  }
}
```

NOTE: both: `https://deckdealer.hopto.org/get/games/name/Blackjack` and `https://deckdealer.hopto.org/get/games?name=Blackjack` will work!

#### We could fetch all games in the `games` table to get the `game_id` for `Blackjack`, and then fetch the `game_id`:
Request:
```jq
https://deckdealer.hopto.org/get/games
```

Response:
```json

{
  "message": "1 game entry found",
  "data": {
    "game_id": 1,
    "name": "Blackjack",
    "min_players": "2",
    "max_players": "10",
    "min_decks": "1",
    "max_decks": "10",
    "player_actions": "setup, hit, stay",
    "rules": "1. All players are dealt 2 cards, 2. Dealer asks each player to \"hit\" or \"stay\", 3. Dealer hits until hand is at least 17, 4. Hand that is closest to 21 but not greater WINS",
    "entry_time": "2022-11-01 21:10:51.915"
  }
}
```

We find that the `game_id` for `Blackjack` is `1`
#### Fetch the `games` table for `game_id=1`:
Arguments:
```rexx
game_id = 1
```

Request:
```jq
https://deckdealer.hopto.org/get/games/game_id/1
```

Response:
```json

{
  "message": "1 game entry found",
  "data": {
    "game_id": 1,
    "name": "Blackjack",
    "min_players": "2",
    "max_players": "10",
    "min_decks": "1",
    "max_decks": "10",
    "player_actions": "setup, hit, stay",
    "rules": "1. All players are dealt 2 cards, 2. Dealer asks each player to \"hit\" or \"stay\", 3. Dealer hits until hand is at least 17, 4. Hand that is closest to 21 but not greater WINS",
    "entry_time": "2022-11-01 21:10:51.915"
  }
}
```

However you wish to make requests is up to you.

</details>

---

### 5.2 - Fetch all registered `users`

<details><summary> (click here to expand) </summary>

#### Fetching all registerd `users`:
Request:
```jq
https://deckdealer.hopto.org/get/users
```

Response:
```json
{
  "message": "found 6 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "dealer", "password": "c00a4b4042678e2dc89247bed50b739c8070dae76a566dd0ecfeb597d8c67d6b1c56b67dd2cd026f11cac24670f23cc6f53a0ea2c25d9f75a0e2142dbaaca2a8", "create_time": "2022-11-01 21:22:46.795"},
    {"user_id": 3, "username": "alice", "password": "2aa046bc10f97c0c11791b538b2a3d06f0dad8308b4ec8ef5166a14723f5ecaac62ab38257981bb7ea095fcb986818b6263082c0ad312a36f0086868833ae5ac", "create_time": "2022-11-01 21:22:47.066"},
    {"user_id": 4, "username": "bob", "password": "b23ee5919bce0a5dd0693f868e50ef5a396bbff79e5c0fa0170eece7536e57a8a95ee8d646ed68491bd2a7acb94e3af388f0bd88650a2a7fadf9cd4c3a44bde1", "create_time": "2022-11-01 21:22:47.201"},
    {"user_id": 5, "username": "anna", "password": "a8afd031b2e7fb99ad5be81e264cdc8dc359795610ae80af3c17fbad8d8aec1136e2a3ddc7e12aa771c5db03141e367e303585961301c44228bcbbdd69d424e7", "create_time": "2022-11-01 21:22:47.360"},
    {"user_id": 6, "username": "steve", "password": "aa19bea81377c41b1089f410db3775f7fbaa005e0ade71f5b4194e0f189bda03c24c95214a3bf2002c0eea97dcfa49869b4254a5c6638b1d0161d5e9a1ce81f7", "create_time": "2022-11-01 21:22:47.497"},
  ],
}
```

</details>

---

### 5.3 - Adding `dealer`, `alice` and `bob` to the `players` table

<details><summary> (click here to expand) </summary>

#### Adding `dealer` to the `players` table:
Arguments:
```rexx
user_id = 2
game_id = 1
name = dealer
email = dealer@udel.edu
```

Request:
```jq
https://deckdealer.hopto.org/add/players/user_id/2/game_id/1/name/dealer/email/dealer@udel.edu
```

Response:
```json
{
  "message": "data added to <players>",
  "player_id": "1",
  "user_id": "2",
  "game_id": "1",
}
```

#### Adding `alice` to the `players` table:
Arguments:
```rexx
user_id = 3
game_id = 1
name = alice
email = alice@udel.edu
```

Request:
```jq
https://deckdealer.hopto.org/add/players/user_id/3/game_id/1/name/alice/email/alice@udel.edu
```

Response:
```json
{
  "message": "data added to <players>",
  "player_id": "2",
  "user_id": "3",
  "game_id": "1",
}
```

#### Adding `bob` to the `players` table:
Arguments:
```rexx
user_id = 4
game_id = 1
name = bob
email = bob@udel.edu
```

Request:
```jq
https://deckdealer.hopto.org/add/players/user_id/4/game_id/1/name/bob/email/bob@udel.edu
```

Response:
```json
{
  "message": "data added to <players>",
  "player_id": "3",
  "user_id": "4",
  "game_id": "1",
}
```

#### Verify that `dealer`, `alice`, and `bob` are in the `players` table:
Request:
```jq
https://deckdealer.hopto.org/get/players
```

Response:
```json
{
  "message": "found 3 player entries",
  "data": [
    {"player_id": 1, "user_id": 2, "game_id": 1, "name": "dealer", "email": "dealer@udel.edu", "entry_time": "2022-11-01 21:54:20.126"},
    {"player_id": 2, "user_id": 3, "game_id": 1, "name": "alice", "email": "alice@udel.edu", "entry_time": "2022-11-01 21:55:16.048"},
    {"player_id": 3, "user_id": 4, "game_id": 1, "name": "bob", "email": "bob@udel.edu", "entry_time": "2022-11-01 21:56:02.308"},
  ],
}
```

</details>

---

### 5.4 - Adding `anna` and `steve` to the `spectators` table

<details><summary> (click here to expand) </summary>

#### Adding `anna` to the `spectators` table:
Arguments:
```rexx
user_id = 5
game_id = 1
name = anna
email = anna@udel.edu
```

Request:
```jq
https://deckdealer.hopto.org/add/spectators/user_id/5/game_id/1/name/anna/email/anna@udel.edu
```

Response:
```json
{
  "message": "data added to <spectators>",
  "spectator_id": "1",
  "user_id": "5",
  "game_id": "1",
}
```

#### Adding `steve` to the `spectators` table:
Arguments:
```rexx
user_id = 6
game_id = 1
name = steve
email = steve@udel.edu
```

Request:
```jq
https://deckdealer.hopto.org/add/spectators/user_id/6/game_id/1/name/steve/email/steve@udel.edu
```

Response:
```json
{
  "message": "data added to <spectators>",
  "spectator_id": "2",
  "user_id": "6",
  "game_id": "1",
}
```

#### Verify that `anna` and `steve` are in the `spectators` table:
Request:
```jq
https://deckdealer.hopto.org/get/spectators
```

Response:
```json
{
  "message": "found 2 spectator entries",
  "data": [
    {"spectator_id": 1, "user_id": 5, "game_id": 1, "name": "anna", "email": "anna@udel.edu", "entry_time": "2022-11-01 22:04:31.979"},
    {"spectator_id": 2, "user_id": 6, "game_id": 1, "name": "steve", "email": "steve@udel.edu", "entry_time": "2022-11-01 22:05:04.008"},
  ],
}
```

</details>

---

### 5.5 - Simulate the first round of play by dealing 2 cards to each user

<details><summary> (click here to expand) </summary>

The `deck` table contains a shuffled deck of 52 cards <br />
We will use this shuffled `deck` to simulate the `bot shuffled cards` <br />

#### Let's examine the top 6 cards of the `deck`:
Arguments:
```rexx
filter = (card_id <= 6)
```

Request:
```erlang
https://deckdealer.hopto.org/get/deck?filter=(card_id <= 6)
```

Response:
```json
{
  "message": "found 6 deck entries",
  "data": [
    {"card_id": 1, "key": "6D", "name": "6", "suit": "DIAMONDS", "description": "6_of_diamonds", "file_name": "6D.png", "entry_time": "2022-11-01 15:04:46.184"},
    {"card_id": 2, "key": "4H", "name": "4", "suit": "HEARTS", "description": "4_of_hearts", "file_name": "4H.png", "entry_time": "2022-11-01 15:04:46.599"},
    {"card_id": 3, "key": "10S", "name": "10", "suit": "SPADES", "description": "10_of_spades", "file_name": "10S.png", "entry_time": "2022-11-01 15:04:46.967"},
    {"card_id": 4, "key": "QH", "name": "QUEEN", "suit": "HEARTS", "description": "queen_of_hearts", "file_name": "QH.png", "entry_time": "2022-11-01 15:04:47.321"},
    {"card_id": 5, "key": "9D", "name": "9", "suit": "DIAMONDS", "description": "9_of_diamonds", "file_name": "9D.png", "entry_time": "2022-11-01 15:04:47.684"},
    {"card_id": 6, "key": "10H", "name": "10", "suit": "HEARTS", "description": "10_of_hearts", "file_name": "10H.png", "entry_time": "2022-11-01 15:04:48.021"},
  ],
}
```

We can see that the `deck` is shuffled <br />

NOTE: When dealing a card to a player, we need to add the entry to the `active_game` table

#### Deal the 1st card to `alice`:
Arguments:
```rexx
game_id = 1
user_id = 3
player_id = 2
player_hand = 6D
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/3/player_id/2/player_hand/6D/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "1",
  "game_id": "1",
  "user_id": "3",
  "player_id": "2",
}
```

#### Deal the 2nd card to `bob`:
Arguments:
```rexx
game_id = 1
user_id = 4
player_id = 3
player_hand = 4H
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/4/player_id/3/player_hand/4H/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "2",
  "game_id": "1",
  "user_id": "4",
  "player_id": "3",
}
```

#### Deal the 3rd card to `dealer`:
Arguments:
```rexx
game_id = 1
user_id = 2
player_id = 1
player_hand = 10S
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/2/player_id/1/player_hand/10S/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "3",
  "game_id": "1",
  "user_id": "2",
  "player_id": "1",
}
```

#### Deal the 4th card to `alice`:
Arguments:
```rexx
game_id = 1
user_id = 3
player_id = 2
player_hand = QH
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/3/player_id/2/player_hand/QH/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "4",
  "game_id": "1",
  "user_id": "3",
  "player_id": "2",
}
```

#### Deal the 5th card to `bob`:
Arguments:
```rexx
game_id = 1
user_id = 4
player_id = 3
player_hand = 9D
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/4/player_id/3/player_hand/9D/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "5",
  "game_id": "1",
  "user_id": "4",
  "player_id": "3",
}
```

#### Deal the 6th card to `dealer`:
Arguments:
```rexx
game_id = 1
user_id = 2
player_id = 1
player_hand = 10H
player_action = setup
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/2/player_id/1/player_hand/10H/player_action/setup
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "6",
  "game_id": "1",
  "user_id": "2",
  "player_id": "1",
}
```

Now the `setup` phase is complete, each `player` has been dealt `2 cards`! <br />

NOTE: recall that when a `user` logs in, their `user_id` is returned. <br />

#### Simulate `alice` fetching her `player_hand`:
Arguments:
```rexx
user_id = 3
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/user_id/3
```

Response:
```json
{
  "message": "found 2 active_game entries",
  "data": [
    {"entry_id": 1, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "6D", "player_action": "setup", "entry_time": "2022-11-01 22:52:08.865"},
    {"entry_id": 4, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "QH", "player_action": "setup", "entry_time": "2022-11-01 22:55:11.283"},
  ],
}
```

#### Simulate `bob` fetching his `player_hand`:
Arguments:
```rexx
user_id = 4
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/user_id/4
```

Response:
```json
{
  "message": "found 2 active_game entries",
  "data": [
    {"entry_id": 2, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "4H", "player_action": "setup", "entry_time": "2022-11-01 22:53:08.192"},
    {"entry_id": 5, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "9D", "player_action": "setup", "entry_time": "2022-11-01 22:55:58.077"},
  ],
}
```

#### Simulate `dealer` fetching their `player_hand`:
Arguments:
```rexx
user_id = 2
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/user_id/2
```

Response:
```json
{
  "message": "found 2 active_game entries",
  "data": [
    {"entry_id": 3, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10S", "player_action": "setup", "entry_time": "2022-11-01 22:54:07.209"},
    {"entry_id": 6, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10H", "player_action": "setup", "entry_time": "2022-11-01 22:57:44.514"},
  ],
}
```

Any user in the `spectators` table can make a generic request to see all `player hands` <br />

#### Simulate a `spectatars` request:
Arguments:
```rexx
filter = (player_id >= 1) ORDER BY player_id
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/filter/(player_id >= 1) ORDER BY player_id
```

Response:
```json
{
  "message": "found 6 active_game entries",
  "data": [
    {"entry_id": 3, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10S", "player_action": "setup", "entry_time": "2022-11-01 22:54:07.209"},
    {"entry_id": 6, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10H", "player_action": "setup", "entry_time": "2022-11-01 22:57:44.514"},
    {"entry_id": 1, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "6D", "player_action": "setup", "entry_time": "2022-11-01 22:52:08.865"},
    {"entry_id": 4, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "QH", "player_action": "setup", "entry_time": "2022-11-01 22:55:11.283"},
    {"entry_id": 2, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "4H", "player_action": "setup", "entry_time": "2022-11-01 22:53:08.192"},
    {"entry_id": 5, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "9D", "player_action": "setup", "entry_time": "2022-11-01 22:55:58.077"},
  ],
}
```

</details>

---

### 5.6 - Simulate each player performing a `player_action` of `hit` or `stay`

<details><summary> (click here to expand) </summary>

Alice has two cards: 6D and QH (6_of_diamonds and Queen_of_Hearts) which totals 16 points. <br />

Alice decides to `hit` <br />

#### Deal the next (7th) card of the `deck`:
Arguments:
```rexx
card_id = 7
```

Request:
```jq
https://deckdealer.hopto.org/get/deck/card_id/7
```

Response:
```json
{
  "message": "1 deck entry found",
  "data": [{"card_id": 7, "key": "3S", "name": "3", "suit": "SPADES", "description": "3_of_spades", "file_name": "3S.png", "entry_time": "2022-11-01 15:04:48.368"}],
}
```

#### Simulate `alice` performing the `hit` action:
Arguments:
```rexx
game_id = 1
user_id = 3
player_id = 2
player_hand = 3S
player_action = hit
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/3/player_id/2/player_hand/3S/player_action/hit
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "7",
  "game_id": "1",
  "user_id": "3",
  "player_id": "2",
}
```

#### Let's examine `alice` current `hand`:
Arguments:
```rexx
player_id = 2
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/player_id/2
```

Response:
```json
{
  "message": "found 3 active_game entries",
  "data": [
    {"entry_id": 1, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "6D", "player_action": "setup", "entry_time": "2022-11-01 22:52:08.865"},
    {"entry_id": 4, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "QH", "player_action": "setup", "entry_time": "2022-11-01 22:55:11.283"},
    {"entry_id": 7, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "3S", "player_action": "hit", "entry_time": "2022-11-01 23:16:10.252"},
  ],
}
```

Alice has three cards: 6D + QH + 3S = `19` points <br />

Alice decides to `stay`, so now it is `bob`'s turn. <br />

Bob has two cards: 4H + 9D = `13` points <br />

Bob decides to `hit` <br />

#### Deal the next (8th) card of the `deck`:
Arguments:
```rexx
card_id = 8
```

Request:
```jq
https://deckdealer.hopto.org/get/deck/card_id/8
```

Response:
```json
{
  "message": "1 deck entry found",
  "data": [{"card_id": 8, "key": "5S", "name": "5", "suit": "SPADES", "description": "5_of_spades", "file_name": "5S.png", "entry_time": "2022-11-01 15:04:48.717"}],
}
```

#### Simulate `bob` performing the `hit` action:
Arguments:
```rexx
game_id = 1
user_id = 4
player_id = 3
player_hand = 5S
player_action = hit
```

Request:
```jq
https://deckdealer.hopto.org/add/active_game/game_id/1/user_id/4/player_id/3/player_hand/5S/player_action/hit
```

Response:
```json
{
  "message": "data added to <active_game>",
  "entry_id": "8",
  "game_id": "1",
  "user_id": "4",
  "player_id": "3",
}
```

#### Let's examine `bob` current `hand`:
Arguments:
```rexx
player_id = 3
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/player_id/3
```

Response:
```json
{
  "message": "found 3 active_game entries",
  "data": [
    {"entry_id": 2, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "4H", "player_action": "setup", "entry_time": "2022-11-01 22:53:08.192"},
    {"entry_id": 5, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "9D", "player_action": "setup", "entry_time": "2022-11-01 22:55:58.077"},
    {"entry_id": 8, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "5S", "player_action": "hit", "entry_time": "2022-11-01 23:31:40.648"},
  ],
}
```

Bob has three cards: 4H + 9D + 5S = `18` points <br />

Bob decides to `stay`, so now it the `dealer`'s turn <br />

Dealer has two cards: 10S + 10H = `20` points <br />

Dealer decides to `stay`. <br />

No more moves can be made, it is now time to determine the winner!

</details>

---

### 5.7 - Determine the winner and add the results to the score_board table

<details><summary> (click here to expand) </summary>

#### Let's combine the `player_hand` for each `player`:
Arguments:
```rexx
filter = (player_id >= 1) ORDER BY player_id
```

Request:
```jq
https://deckdealer.hopto.org/get/active_game/filter/(player_id >= 1) ORDER BY player_id
```

Response:
```json
{
  "message": "found 8 active_game entries",
  "data": [
    {"entry_id": 3, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10S", "player_action": "setup", "entry_time": "2022-11-01 22:54:07.209"},
    {"entry_id": 6, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10H", "player_action": "setup", "entry_time": "2022-11-01 22:57:44.514"},
    {"entry_id": 1, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "6D", "player_action": "setup", "entry_time": "2022-11-01 22:52:08.865"},
    {"entry_id": 4, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "QH", "player_action": "setup", "entry_time": "2022-11-01 22:55:11.283"},
    {"entry_id": 7, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "3S", "player_action": "hit", "entry_time": "2022-11-01 23:16:10.252"},
    {"entry_id": 2, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "4H", "player_action": "setup", "entry_time": "2022-11-01 22:53:08.192"},
    {"entry_id": 5, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "9D", "player_action": "setup", "entry_time": "2022-11-01 22:55:58.077"},
    {"entry_id": 8, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "5S", "player_action": "hit", "entry_time": "2022-11-01 23:31:40.648"},
  ],
}
```

Dealer has 2 cards: 10S + 10H = `20` points <br />
Alice has 3 cards: 6D + QH + 3S = `19` points <br />
Bob has 3 cards: 4H + 9D + 5S = `18` points <br />

**Dealer Wins !!!**

#### Add winner to `score_board` table:
Arguments:
```rexx
game_id = 1
user_id = 2
player_id = 1
winner = dealer
winner_email = dealer@udel.edu
winner_hand = 10S, 10H
winner_score = 20
players = dealer, alice, bob
player_hands = 10S+10H, 6D+QH+3S, 4H+9D+5S
player_scores = 20, 19, 18
spectators = anna, steve
```

Request:
```jq
https://deckdealer.hopto.org/add/score_board/game_id/1/user_id/2/player_id/1/winner/dealer/winner_email/dealer@udel.edu/winner_hand/10S, 10H/winner_score/20/players/dealer, alice, bob/player_hands/10S+10H, 6D+QH+3S, 4H+9D+5S/player_scores/20, 19, 18/spectators/anna, steve
```

Response:
```json
{
  "message": "data added to <score_board>",
  "score_id": 1,
  "game_id": "1",
  "user_id": "2",
  "player_id": "1"
}
```

</details>

</details>

---

# 3. `/edit`
**Edit a single entry or multiple entries of a table**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/edit
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/edit/usage
```
</td><td>

```rexx
returns message: 'usage-info'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}
```
</td><td>

```rexx
returns message: 'missing a parameter'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
edit entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/edit/{table_name}?param_name=param_value
```
</td><td>

```rexx
edit entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/edit/{table_name}/filter/{filter_string}
```
</td><td>

```rexx
edit entries: filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/edit/{table_name}?filter=filter_string
```
</td><td>

```rexx
edit entries: filter='
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
at least 1 edit parameter
```
</td><td>

```rexx
any parameter not *_id or *_time
```
</td></tr><tr></tr><tr><td>

```rexx
at least 1 reference parameter
```
</td><td>

```rexx
any *_id or *_time parameter or filter
```

</td></tr>
</table>


### Response After Successful [`/edit`](#3-edit):
<table>
<tr><td> Variable </td><td> Comment </td></tr><tr><td>

```rexx
message
```
</td><td>

```rexx
number of edits made
```
</td></tr><tr></tr><tr><td>

```rexx
submitted[]
```
</td><td>

```rexx
the parameters that were submitted
```
</td></tr>
</table>

---

<details><summary>Endpint Background (click here to expand)
</summary>


### Investigating the Endpoint: `/edit`
The endpoint to edit a user from the **`users`** is **`/edit/users`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/edit/users
```

Response:
```json
{
    "message": "missing a parameter to edit",
    "editable": [{"username": "TEXT", "password": "TEXT"}],
    "submitted": [{}]
}
```

Making a request with only an **editable_parameter** updates the `missing parameters` message:

Arguments:
```python
username = bob
```

Request:
```ruby
/edit/users/username/bob
```

Response:
```json
{
    "message": "missing a query parameter",
    "query_params": [{"user_id": "INTEGER", "create_time": "DATETIME", "filter": ""}],
    "submitted": [{"username": "bob"}]
}
```

Making a request with only a **query_parameter** also updates the `missing parameters` message:

Arguments:
```python
user_id = 8
```

Request:
```ruby
/edit/users?user_id=8
```

Response:
```json
{
    "message": "missing a parameter to edit",
    "editable": [{"username": "TEXT", "password": "TEXT"}],
    "submitted": [{"user_id": "8"}, {"filter": ""}]
}

```

### Edit bob's **`username`** from `bob` to `robert`
Arguments:
```python
username = robert
user_id = 8
```

Request:
```ruby
/edit/users/username/robert?user_id=8
```

Response:
```json
{
    "message": "edited 1 user entry",
    "submitted": [{"username": "robert", "user_id": "8"}]
}
```

Check the user to verify the edit

Arguments:
```python
user_id = 8
```

Request:
```ruby
/get/users?user_id=8
```

Response:
```json
{
    "message": "1 user entry found",
    "data": {
        "user_id": 8,
        "username": "robert",
        "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
        "create_time": "2022-04-05 03:41:12.857"
    }
}
```

### Appending `@gmail.com` to the **`username`** for both `robert` and `alice`
Arguments:
```python
username = username||"@gmail.com"
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/edit/users/username/username||"@gmail.com"?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "edited 2 user entries",
    "submitted": [{
        "filter": "(user_id=\"7\" OR user_id=\"8\")",
        "username": "username||\"@gmail.com\""
    }]
}
```

Verify the edits

Arguments:
```python
filter = (user_id="7" OR user_id="8")
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/get/users?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "found 2 user entries",
    "data": [
        {
            "user_id": 7,
            "username": "alice@gmail.com",
            "password": "df564e993decffa1a96454f7fa0dc48f0bf66c981f141aaf9b140f18c7f3aed90727ec05e4fcef23af66830dd6883b6b899414eff98aa2669443bc8d42470c9a",
            "create_time": "2022-04-05 03:25:57.163"
        },
        {
            "user_id": 8,
            "username": "robert@gmail.com",
            "password": "8ca79597eb2bc1eebd93a1d595e921fcc64a2c00f175cc5dfa59a728122bc846f1bba08457795d539145508d99747a43049cee0c0f696c7d1b088131b45fa0d4",
            "create_time": "2022-04-05 03:41:12.857"
        }
    ]
}
```

### Replacing all **`users`** with **`username`** containing `@gmail.com` to `@udel.edu`
Arguments:
```python
username = REPLACE(username, "@gmail.com", "@udel.edu")
filter = (user_id="7" OR user_id="8")
```

Request:
```ruby
/edit/users/username/REPLACE(username, "@gmail.com", "@udel.edu")?filter=(user_id="7" OR user_id="8")
```

Response:
```json
{
    "message": "edited 2 user entries",
    "submitted": [{
        "filter": "(user_id=\"7\" OR user_id=\"8\")",
        "username": "REPLACE(username, \"@gmail.com\", \"@udel.edu\")"
    }]
}
```

Verify the edits

### Converting the **`temperature`** from **`farenheight`** to **`celsius`** for `alice`
> Note: parsing url paths now support fractions :)

Arguments:
```python
temperature = ((5.0/9.0)*(temperature-32.0))
filter = (user_id="7")
```

Request:
```ruby
/edit/oximeter/temperature/(temperature-32.0)*(5.0/9.0)?filter=(user_id="7")
```

Response:
```json
{
    "message": "edited 6 oximeter entries",
    "submitted": [{
        "filter": "(user_id=\"7\")",
        "temperature": "((5.0/9.0)*(temperature-32.0))"
    }]
}
```

Verify the edits

Arguments:
```python
filter = (user_id="7")
```

Request:
```ruby
/get/oximeter?filter=(user_id="7")
```

Response:
```json
{
    "message": "found 6 oximeter entries",
    "data": [
        {"entry_id": 43, "user_id": 7, "heart_rate": 134, "blood_o2": 97, "temperature": 36.48286879954039, "entry_time": "2022-04-05 12:06:01.397"},
        {"entry_id": 44, "user_id": 7, "heart_rate": 129, "blood_o2": 98, "temperature": 36.36295123460418, "entry_time": "2022-04-05 12:06:01.528"},
        {"entry_id": 45, "user_id": 7, "heart_rate": 128, "blood_o2": 100, "temperature": 36.30975186413218, "entry_time": "2022-04-05 12:06:01.740"},
        {"entry_id": 46, "user_id": 7, "heart_rate": 134, "blood_o2": 96, "temperature": 36.13161890536411, "entry_time": "2022-04-05 12:06:01.994"},
        {"entry_id": 47, "user_id": 7, "heart_rate": 132, "blood_o2": 96, "temperature": 36.54783110302192, "entry_time": "2022-04-05 12:06:02.469"},
        {"entry_id": 48, "user_id": 7, "heart_rate": 130, "blood_o2": 98, "temperature": 36.257128704506115, "entry_time": "2022-04-05 12:06:02.669"}
    ]
}
```

</details>

---

## [Workflow 6 - Editing Data](#Workflow-6---Editing-Data)

---

<details><summary> (click here to expand) </summary>

### Executing a Profile Edit

#### `anna` and `steve` would like to edit their `username` to use their `email` and update their `password`

#### Let's start with `anna`

#### `anna` would like to change her `username` from `anna` to `anna@udel.edu` and her `password` from `anna` to `Anna1234`

#### Query the `users` table to see all of the current `users`:
Request:
```jq
https://deckdealer.hopto.org/get/users
```

Response:
```json
{
  "message": "found 6 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "756a404bd66b7f081a936fe6fbcf2374de5c6ce018d62f37e664be8df02de03807b51fc4273dc06d12c11f7075369b5e96e2b0fef57037f6711f7e0f07a224af", "create_time": "2022-10-28 09:34:39.683"},
    {"user_id": 2, "username": "dealer", "password": "c00a4b4042678e2dc89247bed50b739c8070dae76a566dd0ecfeb597d8c67d6b1c56b67dd2cd026f11cac24670f23cc6f53a0ea2c25d9f75a0e2142dbaaca2a8", "create_time": "2022-11-01 21:22:46.795"},
    {"user_id": 3, "username": "alice", "password": "2aa046bc10f97c0c11791b538b2a3d06f0dad8308b4ec8ef5166a14723f5ecaac62ab38257981bb7ea095fcb986818b6263082c0ad312a36f0086868833ae5ac", "create_time": "2022-11-01 21:22:47.066"},
    {"user_id": 4, "username": "bob", "password": "b23ee5919bce0a5dd0693f868e50ef5a396bbff79e5c0fa0170eece7536e57a8a95ee8d646ed68491bd2a7acb94e3af388f0bd88650a2a7fadf9cd4c3a44bde1", "create_time": "2022-11-01 21:22:47.201"},
    {"user_id": 5, "username": "anna", "password": "a8afd031b2e7fb99ad5be81e264cdc8dc359795610ae80af3c17fbad8d8aec1136e2a3ddc7e12aa771c5db03141e367e303585961301c44228bcbbdd69d424e7", "create_time": "2022-11-01 21:22:47.360"},
    {"user_id": 6, "username": "steve", "password": "aa19bea81377c41b1089f410db3775f7fbaa005e0ade71f5b4194e0f189bda03c24c95214a3bf2002c0eea97dcfa49869b4254a5c6638b1d0161d5e9a1ce81f7", "create_time": "2022-11-01 21:22:47.497"},
  ],
}
```

#### Changing the `username` and `password` for `anna`:
Arguments:
```rexx
username = anna@udel.edu
password = Anna1234
filter = (user_id=5)
```

Request:
```erlang
https://deckdealer.hopto.org/edit/users/username/anna@udel.edu/password/Anna1234/?filter=(user_id=5)
```

Response:
```json
{
  "message": "edited 1 user entry",
  "submitted": [
    {
      "filter": "(user_id=5)",
      "username": "anna@udel.edu",
      "password": "96205a4208c729325fdc3de16fe7549dac2040162ecc311321c1e193815a0cf5f9fc8e18084f648a87a0df389d4250f40cbfd5053b83f23ccfc2b59a5ee16aec"
    }
  ]
}
```

#### Verify by logging in with the new `username` and `password`:
Arguments:
```rexx
username = anna@udel.edu
password = Anna1234
```

POST Request:
```jq
POST(url="https://deckdealer.hopto.org/login", data={"username": "anna@udel.edu", "password": "Anna1234"})
```

OR GET Request:
> GET Request will not store session client side...
> If you don't want to deal with sessions, I can disable this feature...
```jq
https://deckdealer.hopto.org/login/username/anna@udel.edu/password/Anna1234
```

Response:
```json
{
  "message": "user login success",
  "user_id": "5",
  "username": "anna@udel.edu",
  "token": "IURBdXFSODZvRXByQ0ZDK2VJNGdXV3c9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFMWxJYVVMZz09",
}
```

#### `steve` would like to change his `username` to `steve@gmail.com` and his `password` to `St3ve4321`

#### Changing the `username` and `password` for `steve`:
Arguments:
```rexx
username = steve@udel.edu
password = St3ve4321
filter = (user_id=6)
```

Request:
```erlang
https://deckdealer.hopto.org/edit/users/?username=steve@udel.edu&password=St3ve4321&filter=(user_id=6)
```

Response:
```json
{
  "message": "edited 1 user entry",
  "submitted": [
    {
      "filter": "(user_id=6)",
      "username": "steve@udel.edu",
      "password": "42b52be908f40c123f5821925c0d5d34c24035518cc65b64295ae8bedd57855bda4555dd855d1fa52255667437c7c521bd545a527cedb099e4813d925482a4f6"
    }
  ]
}
```

#### Verify by logging in with the new `username` and `password`:
Arguments:
```rexx
username = steve@gmail.com
password = St3ve4321
```

POST Request:
```jq
POST(url="https://deckdealer.hopto.org/login", data={"username": "steve@gmail.com", "password": "St3ve4321"})
```

OR GET Request:
> GET Request will not store session client side...
> If you don't want to deal with sessions, I can disable this feature...
```erlang
https://deckdealer.hopto.org/login/?username=steve@udel.edu&password=St3ve4321
```

Response:
```json
{
  "message": "user login success",
  "user_id": "6",
  "username": "steve@udel.edu",
  "token": "IUF5K2NMZTg4eWZBd0g2TVNvL1BFelE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFMmxJYVVMZz09",
}
```

</details>

---


# 4. `/delete`
**Delete a single entry or multiple entries of a table**

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr><tr><td>

```jq
/delete
```
</td><td>

```rexx
returns all tables[] in the database
```
</td></tr><tr></tr><tr><td>

```jq
/delete/usage
```
</td><td>

```rexx
returns message: 'usage-info'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}
```
</td><td>

```rexx
returns message: 'missing a parameter'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}/{param_name}/{param_value}
```
</td><td>

```rexx
delete entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```erlang
/delete/{table_name}?param_name=param_value
```
</td><td>

```rexx
delete entries: 'param_name=param_value'
```
</td></tr><tr></tr><tr><td>

```jq
/delete/{table_name}/filter/{filter_string}
```
</td><td>

```rexx
delete entries: filter='
```
</td></tr><tr></tr><tr><td>

```erlang
/delete/{table_name}?filter=filter_string
```
</td><td>

```rexx
delete entries: filter='
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Comment </td></tr><tr><td>

```rexx
at least 1 reference parameter
```
</td><td>

```rexx
any *_id or *_time parameter or filter
```
</td></tr>
</table>


### Response After Successful [`/delete`](#4-delete):
<table>
<tr><td> Variable </td><td> Comment </td></tr>
<tr><td>

```rexx
message
```

</td><td>

```rexx
number of deletes made
```

</td></tr><tr></tr><tr><td>

```rexx
submitted[]
```

</td><td>

```rexx
the parameters that were submitted
```

</td></tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/delete`
The endpoint for deleting an entry from the **`oximeter`** table is **`/delete/oximeter`**.
Making a request to the endpoint without providing **parameters** returns a `missing parameters` message:

Request:
```ruby
/delete/oximeter
```

Response:
```json
{
    "message": "missing a query param(s)",
    "query_params": [
        {"entry_id": "INTEGER", "user_id": "INTEGER", "heart_rate": "INTEGER", "blood_o2": "INTEGER", "temperature": "DOUBLE", "entry_time": "DATETIME", "filter": ""}
    ],
    "submitted": [{}]
}
```

### Deleting all entries for `Robert` with **`temperature`** in the fever range
Arguments:
```python
filter = (user_id = "8" AND temperature > "100.4")
```

Request:
```ruby
/delete/oximeter?filter=(user_id = "8" AND temperature > "100.4")
```

Response:
```json
{
    "message": "6 oximeter entries deleted",
    "submitted": [{"filter": "(user_id = \"8\" AND temperature > \"100.4\")"}]
}
```

Verify the deletes

Arguments:
```python
user_id = 8
```

Request:
```ruby
/get/oximeter/user_id/8
```

Response:
```json
{
    "message": "found 4 oximeter entries",
    "data": [
        {"entry_id": 49, "user_id": 8, "heart_rate": 143, "blood_o2": 97, "temperature": 97.23579109761334, "entry_time": "2022-04-05 12:16:11.420"},
        {"entry_id": 50, "user_id": 8, "heart_rate": 127, "blood_o2": 97, "temperature": 97.7532770488335, "entry_time": "2022-04-05 12:16:11.592"},
        {"entry_id": 51, "user_id": 8, "heart_rate": 131, "blood_o2": 95, "temperature": 97.89202180155488, "entry_time": "2022-04-05 12:16:11.747"},
        {"entry_id": 52, "user_id": 8, "heart_rate": 124, "blood_o2": 95, "temperature": 97.81020200542864, "entry_time": "2022-04-05 12:16:11.897"}
    ]
}
```
</details>

---

## [Workflow 7 - Deleting Data](#Workflow-7---Deleting-Data)

---

<details><summary> (click me to exapnd) </summary>

### Clean up the entries in the `active_game` table to finish the `Blackjack` game from [Workflow 5](#workflow-5---requesting-data)

#### After the `Blackjack` game ended, we added the results to the `score_board` table but we left the logs in the `active_game` table.
#### Before we can start a new game, we should delete the entries in the `active_game` table.
#### I didn't create a table for keeping old game logs, but it shouldn't be too hard to do now that you have made it here :)

#### Let's examine the `score_board` table to make sure that the winning results from our game is there:
Request:
```jq
https://deckdealer.hopto.org/get/score_board
```

Response:
```json

{
  "message": "1 score_board entry found",
  "data": {
    "score_id": 1,
    "game_id": 1,
    "user_id": 2,
    "player_id": 1,
    "winner": "dealer",
    "winner_email": "dealer@udel.edu",
    "winner_hand": "10S, 10H",
    "winner_score": 20,
    "players": "dealer, alice, bob",
    "player_hands": "10S+10H, 6D+QH+3S, 4H+9D+5S",
    "player_scores": "20, 19, 18",
    "spectators": "anna, steve",
    "entry_time": "2022-11-02 11:28:11.442"
  }
}
```

We see that the `dealer` won with a hand of `10S+10H` and a score of `20` <br />

#### Now let's check the `active_game` table to see if the logs are still there:
Request:
```jq
https://deckdealer.hopto.org/get/active_game
```

Response:
```json
{
  "message": "found 8 active_game entries",
  "data": [
    {"entry_id": 1, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "6D", "player_action": "setup", "entry_time": "2022-11-01 22:52:08.865"},
    {"entry_id": 2, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "4H", "player_action": "setup", "entry_time": "2022-11-01 22:53:08.192"},
    {"entry_id": 3, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10S", "player_action": "setup", "entry_time": "2022-11-01 22:54:07.209"},
    {"entry_id": 4, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "QH", "player_action": "setup", "entry_time": "2022-11-01 22:55:11.283"},
    {"entry_id": 5, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "9D", "player_action": "setup", "entry_time": "2022-11-01 22:55:58.077"},
    {"entry_id": 6, "game_id": 1, "user_id": 2, "player_id": 1, "player_hand": "10H", "player_action": "setup", "entry_time": "2022-11-01 22:57:44.514"},
    {"entry_id": 7, "game_id": 1, "user_id": 3, "player_id": 2, "player_hand": "3S", "player_action": "hit", "entry_time": "2022-11-01 23:16:10.252"},
    {"entry_id": 8, "game_id": 1, "user_id": 4, "player_id": 3, "player_hand": "5S", "player_action": "hit", "entry_time": "2022-11-01 23:31:40.648"},
  ],
}
```

Looks like the log entries are still there! <br />

#### Let's delete all entries from the `active_game` table:
Arguments:
```rexx
filter = (entry_id >= 1)
```

Request:
```erlang
https://deckdealer.hopto.org/delete/active_game?filter=(entry_id >= 1)
```

Response:
```json
{
  "message": "8 active_game entries deleted",
  "submitted": [{"filter": "(entry_id >= 1)"}],
}
```

#### Verify that there are no entries in the `active_game` table:
Request:
```jq
https://deckdealer.hopto.org/get/active_game
```

Response:
```json

{
  "message": "0 active_game entries found using submitted parameters",
  "data": {
    "submitted": [
      {},
      {
        "filter": ""
      }
    ]
  }
}
```

</details>

---


# [Extra Functions](#Extra-Functions)
The examples listed below will cover the **1 extra function**.<br />
All examples shown are executed via a **GET** request and can be tested with any browser. <br />
All endpoints support 4 *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

# 1. `/uploadImageUrl`
**Upload an image to the backend via image url** 

### Endpoints:
<table>
<tr><td> Resource </td><td> Description </td></tr>
<tr><td>

```jq
/uploadImageUrl
```
</td><td>

```rexx
returns: {"message": "missing parameters", "required params": ["url"]}
```
</td></tr>
<tr></tr><tr><td>

```jq
/uploadImageUrl/usage
```
</td><td>

```rexx
returns: {"message": "usage_info"}
```
</td></tr>
<tr></tr><tr><td>

```jq
/uploadImageUrl/<param_name>/<param_value>
```
</td><td>

```rexx
upload with url_paths: 'param_name=param_value'
```
</td></tr>
<tr></tr>
<tr><td>

```jq
/uploadImageUrl?param_name=param_value
```
</td><td>

```rexx
upload with params: 'param_name=param_value'
```
</td></tr>
</table>


### Requirements:
<table>
<tr><td> Parameters </td><td> Description </td></tr>
<tr>
<td>

```rexx
url
```

</td>
<td>

```rexx
the full url path of the image you wish to upload and save into the backend
```

</td>
</tr>
</table>

---

<details><summary>Endpoint Background (click here to expand)</summary>

### Investigating the Endpoint: `/uploadImageUrl`
Request:
```jq
https://deckdealer.hopto.org/uploadImageUrl
```

Response:
```json
{
  "message": "missing parameters",
  "required": [["url"]],
  "submitted": [{}],
}
```

Request:
```ruby
/uploadImageUrl/usage
```

Response:
```json
{
  "message": "usage info: /uploadImageUrl",
  "description": "upload an image to the backend via image url",
  "end_points": {
    "/uploadImageUrl": {
      "returns": "missing paramaters"
    },
    "/uploadImageUrl/usage": {
      "returns": "message: 'usage-info'"
    },
    "/uploadImageUrl/<param_name>/<param_value>": {
      "url_paths": "upload with: 'param_name=param_value'",
      "example": "/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
      "response": {
        "message": "image url uploaded",
        "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
        "filename": "/static/img/2.png"
      }
    },
    "/uploadImageUrl?param_name=param_value": {
      "url_paths": "upload with: 'param_name=param_value'",
      "example": "/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
      "response": {
        "message": "image url uploaded",
        "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
        "filename": "/static/img/2.png"
      }
    },
    "Required": {
      "Parameters": {
        "url": "TEXT"
      }
    },
    "Response": {
      "message": "image url uploaded",
      "url": "TEXT",
      "filename": "TEXT"
    }
  }
}
```

Arguments:
```python
url = "https://deckdealer.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png"
```

Request:
```ruby
https://deckdealer.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
  "filename": "/static/img/1.png"
}
```

</details>

---
