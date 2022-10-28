# [Web Framework](#Web-Framework)
[https://bartender.hopto.org](https://bartender.hopto.org)

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
https://bartender.hopto.org/add
https://bartender.hopto.org/get
https://bartender.hopto.org/edit
https://bartender.hopto.org/delete
https://bartender.hopto.org/createTable
https://bartender.hopto.org/deleteTable
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

If you receive an `invalid token` response, then the request you are making does not contain the `session cookie`.
**REQUESTS TO `/login` SHOULD BE DONE AS A `POST` REQUEST**
The `session cookie` is assigned after a successful login.
To get around adding the `session cookie` along with your request, you can simply add the `token` parameter.

FOR EXAMPLE:

### You logged in with the `admin` user.
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

### All requests returning `invalid token`?
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

### Simply append the token parameter
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
curl -XPOST -b cookie.txt -c cookie.txt 'http://bartender.hopto.org/login' -d '{"username": "admin", "password": "admin"}'
curl -b cookie.txt -c cookie.txt 'http://bartender.hopto.org/get/users'
```
</p>
</details>

---

# [Getting Started](#Getting-Started)
Follow the [Setup Guide](SERVER_SETUP.md) to install and configure the framework. <br />

You can choose to run the server locally or connect with the server all ready running at: <br />
[https://bartender.hopto.org](https://bartender.hopto.org)

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
POST(url='https://bartender.hopto.org/login', data={"username": "admin", "password": "admin"})
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

> Note: the `token` is only needed when api requests do not store session cookies.

### Verify session by making a request to `/status`
Request:
```jq
https://bartender.hopto.org/status
```

Response:
```json
{
  "message": "user is logged in with valid session",
  "user_id": "3",
  "cookies": {
    "user_id": "!Immfx4DNO8Eu23dwT1qvIA==?gASVEQAAAAAAAACMB3VzZXJfaWSUjAEzlIaULg=="
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

### Let's create a few users by registering them: `alice`, `bob`, `anna`, `steve`
---

Arguments:
```rexx
username = alice
password = alice
password2 = alice
```

Request:
```jq
https://bartender.hopto.org/register/username/alice/password/alice/password2/alice
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
https://bartender.hopto.org/register/username/bob/password/bob/password2/bob
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
https://bartender.hopto.org/register/username/anna/password/anna/password2/anna
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
https://bartender.hopto.org/register/username/steve/password/steve/password2/steve
```

Response:
```json
{"message": "new user created", "user_id": 5, "username": "steve"}
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

### Let's create a few tables!<br />
<table>
<tr><td> Table Name </td><td> Column Names </td></tr><tr><td>

```rexx
managers
```
</td><td>

```jq
["manager_id", "user_id", "first_name", "last_name", "phone_number", "email", "profile_pic", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
restaurant_profile
```
</td><td>

```jq
["restaurant_id", "manager_id", "restaurant_name", "address", "bio", "phone_number", "profile_pic", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
restaurant_schedule
```
</td><td>

```jq
["schedule_id", "restaurant_id", "mon_open", "mon_close", "tue_open", "tue_close", "wed_open", "wed_close", "thu_open", "thu_close", "fri_open", "fri_close", "sat_open", "sat_close", "sun_open", "sun_close", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
restaurant_requests
```
</td><td>

```jq
["request_id", "restaurant_id", "hourly_wage", "shift_start", "shift_end", "status", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
restaurant_photos
```

</td><td>

```jq
["photo_id", "restaurant_id", "file_name", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
bartenders
```
</td><td>

```jq
["bartender_id", "user_id", "first_name", "last_name", "address", "phone_number", "email", "profile_pic", "entry_time"]
```
</td></tr><tr></tr><tr><td>

```rexx
bartender_shifts
```
</td><td>

```jq
["shift_id", "bartender_id", "restaurant_id", "request_id", "shift_start", "shift_end", "entry_time"]
```
</td></tr>
<tr></tr><tr><td>

```rexx
bartender_wages
```
</td><td>

```jq
["wage_id", "bartender_id", "shift_id", "restaurant_id", "hourly_wage", "shift_start", "shift_end", "clock_in", "clock_out", "hours_worked", "tips", "total_earnings", "entry_time"]
```
</td></tr>
</table>

---

### Creating the Table `managers`:
Request:
```ruby
https://bartender.hopto.org/createTable/managers/manager_id/INTEGER/user_id/INTEGER/first_name/TEXT/last_name/TEXT/phone_number/TEXT/email/TEXT/profile_pic/TEXT/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "managers",
    "columns": [
        "manager_id INTEGER PRIMARY KEY",
        "user_id INTEGER NOT NULL",
        "first_name TEXT NOT NULL",
        "last_name TEXT NOT NULL",
        "phone_number TEXT NOT NULL",
        "email TEXT NOT NULL",
        "profile_pic TEXT NOT NULL",
        "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `restaurant_profile`:
Request:
```ruby
https://bartender.hopto.org/createTable/restaurant_profile/restaurant_id/INTEGER/manager_id/INTEGER/restaurant_name/TEXT/address/TEXT/bio/TEXT/phone_number/TEXT/profile_pic/TEXT/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "restaurant_profile",
    "columns": [
        "restaurant_id INTEGER PRIMARY KEY",
        "manager_id INTEGER NOT NULL",
        "restaurant_name TEXT NOT NULL",
        "address TEXT NOT NULL",
        "bio TEXT NOT NULL",
        "phone_number TEXT NOT NULL",
        "profile_pic TEXT NOT NULL",
        "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `restaurant_photos`:
Request:
```ruby
https://bartender.hopto.org/createTable/restaurant_photos/photo_id/INTEGER/restaurant_id/INTEGER/file_name/TEXT/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "restaurant_photos",
    "columns": ["photo_id INTEGER PRIMARY KEY", "restaurant_id INTEGER NOT NULL", "file_name TEXT NOT NULL", "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"]
}
```

### Creating the Table `restaurant_schedule`:
Request:
```ruby
https://bartender.hopto.org/createTable/restaurant_schedule/schedule_id/INTEGER/restaurant_id/INTEGER/mon_open/DATETIME/mon_close/DATETIME/tue_open/DATETIME/tue_close/DATETIME/wed_open/DATETIME/wed_close/DATETIME/thu_open/DATETIME/thu_close/DATETIME/fri_open/DATETIME/fri_close/DATETIME/sat_open/DATETIME/sat_close/DATETIME/sun_open/DATETIME/sun_close/DATETIME/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "restaurant_schedule",
    "columns": [
        "schedule_id INTEGER PRIMARY KEY", "restaurant_id INTEGER NOT NULL",
        "mon_open DATETIME NOT NULL", "mon_close DATETIME NOT NULL",
        "tue_open DATETIME NOT NULL", "tue_close DATETIME NOT NULL",
        "wed_open DATETIME NOT NULL", "wed_close DATETIME NOT NULL",
        "thu_open DATETIME NOT NULL", "thu_close DATETIME NOT NULL",
        "fri_open DATETIME NOT NULL", "fri_close DATETIME NOT NULL",
        "sat_open DATETIME NOT NULL", "sat_close DATETIME NOT NULL",
        "sun_open DATETIME NOT NULL", "sun_close DATETIME NOT NULL",
        "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `restaurant_requests`:
> NOTE: `status` is used to indicate the current state of a `request`
> **`status` states**
> |     State | Description   |
> |---:|:---|
> |      open | Available for snagging... no bartender has picked this shift up yet. |
> |   snagged | A bartender has snagged this shift but not yet completed it... see table [bartender_shifts](#Creating-the-Table-bartender_shifts) |
> | completed | The bartender that snagged the request has worked the shift... see table [bartender_wages](#Creating-the-Table-bartender_wages)  |

Request:
```jq
https://bartender.hopto.org/createTable/restaurant_requests/request_id/INTEGER/restaurant_id/INTEGER/hourly_wage/DOUBLE/shift_start/DATETIME/shift_end/DATETIME/status/TEXT/entry_time/DATETIME
```

Response:
```json
{
  "message": "1 table created",
  "table": "restaurant_requests",
  "columns": [
    "request_id INTEGER PRIMARY KEY",
    "restaurant_id INTEGER NOT NULL",
    "hourly_wage DOUBLE NOT NULL",
    "shift_start DATETIME NOT NULL",
    "shift_end DATETIME NOT NULL",
    "status TEXT NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ]
}
```

### Creating the Table `bartenders`:
Request:
```ruby
https://bartender.hopto.org/createTable/bartenders/bartender_id/INTEGER/user_id/INTEGER/first_name/TEXT/last_name/TEXT/address/TEXT/phone_number/TEXT/email/TEXT/profile_pic/TEXT/entry_time/DATETIME
```

Response:
```json
{
    "message": "1 table created",
    "table": "bartenders",
    "columns": [
        "bartender_id INTEGER PRIMARY KEY",
        "user_id INTEGER NOT NULL",
        "first_name TEXT NOT NULL",
        "last_name TEXT NOT NULL",
        "address TEXT NOT NULL",
        "phone_number TEXT NOT NULL",
        "email TEXT NOT NULL",
        "profile_pic TEXT NOT NULL",
        "entry_time DATETIME NOT NULL DEFAULT (strftime(\"%Y-%m-%d %H:%M:%f\", \"now\", \"localtime\"))"
    ]
}
```

### Creating the Table `bartender_shifts`:
Request:
```jq
https://bartender.hopto.org/createTable/bartender_shifts/shift_id/INTEGER/bartender_id/INTEGER/restaurant_id/INTEGER/request_id/INTEGER/shift_start/DATETIME/shift_end/DATETIME/entry_time/DATETIME
```

Response:
```json
{
  "message": "1 table created",
  "table": "bartender_shifts",
  "columns": [
    "shift_id INTEGER PRIMARY KEY",
    "bartender_id INTEGER NOT NULL",
    "restaurant_id INTEGER NOT NULL",
    "request_id INTEGER NOT NULL",
    "shift_start DATETIME NOT NULL",
    "shift_end DATETIME NOT NULL",
    "entry_time DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
  ]
}
```

### Creating the Table `bartender_wages`:
Request:
```jq
https://bartender.hopto.org/createTable/bartender_wages/wage_id/INTEGER/bartender_id/INTEGER/shift_id/INTEGER/restaurant_id/INTEGER/hourly_wage/DOUBLE/shift_start/DATETIME/shift_end/DATETIME/clock_in/DATETIME/clock_out/DATETIME/hours_worked/DOUBLE/tips/DOUBLE/total_earnings/DOUBLE/entry_time/DATETIME
```

Response:
```json
{
  "message": "1 table created",
  "table": "bartender_wages",
  "columns": [
    "wage_id INTEGER PRIMARY KEY",
    "bartender_id INTEGER NOT NULL",
    "shift_id INTEGER NOT NULL",
    "restaurant_id INTEGER NOT NULL",
    "hourly_wage DOUBLE NOT NULL",
    "shift_start DATETIME NOT NULL",
    "shift_end DATETIME NOT NULL",
    "clock_in DATETIME NOT NULL",
    "clock_out DATETIME NOT NULL",
    "hours_worked DOUBLE NOT NULL",
    "tips DOUBLE NOT NULL",
    "total_earnings DOUBLE NOT NULL",
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

### Assigning `users` to `Roles` and creating `User Profiles`
1. Lets upload profile pictures for the 4 users we added earlier and 2 reqtaurants...
2. `alice` and `bob` are managers at `Iron Hill` and `Deer Park`; let's add them to the **`managers`** table
3. `anna` and `steve` are bartenders; let's add them to the **`bartenders`** table

### Setting up the `Restaurant Tables`
4. Add `Iron Hill` and `Deer Park` to the `restaurant_profile` and `restaurant_photos` tables
5. Then add their schedules to the `restaurant_schedule` table

### Simulate `Restaurant Requests`
6. Log in as a `manager` and create a `shift request` into the `restaurant_requests` table

---

### 4.1 - Uploading Profile Pictures

<details><summary> (click here to expand) </summary>

<br />We can use the endpoint `/uploadImageUrl/url/<url>` to upload profile pictures...

---
#### Uploading profile picture for `alice`:
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar4.png
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar4.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar4.png",
  "full_path": "/static/img/1.png",
  "file_name": "1.png"
}
```
---
#### Uploading profile picture for `bob`:
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar2.png
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar2.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar2.png",
  "full_path": "/static/img/2.png",
  "file_name": "2.png"
}
```
---
#### Uploading profile picture for `anna`:
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar5.png
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar5.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar5.png",
  "full_path": "/static/img/3.png",
  "file_name": "3.png"
}
```
---
#### Uploading profile picture for `steve`:
Arguments:
```rexx
url = https://www.w3schools.com/w3images/avatar3.png
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.w3schools.com/w3images/avatar3.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.w3schools.com/w3images/avatar3.png",
  "full_path": "/static/img/4.png",
  "file_name": "4.png"
}
```
---
#### Uploading profile picture for `Iron Hill`:
Arguments:
```rexx
url = https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
  "full_path": "/static/img/5.png",
  "file_name": "5.png"
}
```
---
#### Uploading profile picture for `Deer Park`:
Arguments:
```rexx
url = https://popmenucloud.com/cdn-cgi/image/width=300,height=300,format=auto,fit=scale-down/jciwfypa/ef5aec3e-af44-4f35-bdf9-b0a855c09328.jpg
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://popmenucloud.com/cdn-cgi/image/width=300,height=300,format=auto,fit=scale-down/jciwfypa/ef5aec3e-af44-4f35-bdf9-b0a855c09328.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://popmenucloud.com/cdn-cgi/image/width=300,height=300,format=auto,fit=scale-down/jciwfypa/ef5aec3e-af44-4f35-bdf9-b0a855c09328.jpg",
  "full_path": "/static/img/6.jpeg",
  "file_name": "6.jpeg"
}
```
---
#### Uploading photos for `Iron Hill`:
Arguments:
```rexx
url = https://www.ironhillbrewery.com/assets/craft/_locationPic1x/locations_0005_newark.jpg
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/_locationPic1x/locations_0005_newark.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.ironhillbrewery.com/assets/craft/_locationPic1x/locations_0005_newark.jpg",
  "full_path": "/static/img/7.jpeg",
  "file_name": "7.jpeg"
}
```

Arguments:
```rexx
url = https://www.ironhillbrewery.com/assets/craft/IMG_7690-2.jpg
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/IMG_7690-2.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://www.ironhillbrewery.com/assets/craft/IMG_7690-2.jpg",
  "full_path": "/static/img/8.jpeg",
  "file_name": "8.jpeg"
}
```
---
#### Uploading photos for `Deer Park`:
Arguments:
```rexx
url = https://popmenucloud.com/jciwfypa/865660db-c7fd-4d06-bf3b-0ee4843caa25.jpg
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://popmenucloud.com/jciwfypa/865660db-c7fd-4d06-bf3b-0ee4843caa25.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://popmenucloud.com/jciwfypa/865660db-c7fd-4d06-bf3b-0ee4843caa25.jpg",
  "full_path": "/static/img/9.jpeg",
  "file_name": "9.jpeg"
}
```

Arguments:
```rexx
url = https://popmenucloud.com/jciwfypa/0a3a3426-0fc1-42bd-8fd8-5e4ec7250aff.jpg
```

Request:
```erlang
https://bartender.hopto.org/uploadImageUrl?url=https://popmenucloud.com/jciwfypa/0a3a3426-0fc1-42bd-8fd8-5e4ec7250aff.jpg
```

Response:
```json
{
  "message": "image url uploaded",
  "url": "https://popmenucloud.com/jciwfypa/0a3a3426-0fc1-42bd-8fd8-5e4ec7250aff.jpg",
  "full_path": "/static/img/10.jpeg",
  "file_name": "10.jpeg"
}
```

</details>

---

### 4.2 - Adding `alice` and `bob` to `managers` table
<details><summary> (click here to expand) </summary>

<br />To assign `alice` and `bob` as managers, we will need their `user_id`.

---
To get info of all users, make a request to the `users` table

Request:
```jq
https://bartender.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {
      "user_id": 1,
      "username": "admin",
      "password": "a2025bd8b86a53fccf6f42eae008ccbf65dcf6aa55e0e6a477b57c5d74b1e611e5902fe9673d8cddb84896005e125d589e39e258a7fbeb3e7208b866e7746e60",
      "create_time": "2022-10-19 00:23:52.930"
    },
    {
      "user_id": 2,
      "username": "alice",
      "password": "b71dab3e13191834f1f0dd53c8b4be30da005ee7eea47ec8673d41c5ee959be34881a9ac99d473bec40b2de489e83694e5e532babbdcfc16c93d137872cffa96",
      "create_time": "2022-10-21 10:06:45.643"
    },
    {
      "user_id": 3,
      "username": "bob",
      "password": "7e6c183ddaf351a96fc6541b6ece83ea130c34ff8151a7e219d7bebace3398d685809c999065a54c7c1c785a4ae5b230f247cae5c97b958c7b881c86e81c3e07",
      "create_time": "2022-10-21 10:06:45.830"
    },
    {
      "user_id": 4,
      "username": "anna",
      "password": "a0d7bf58601f8f515eb56fb80ec986e49e40eb96572f33abab6ce924c7b3cd0d3cadeb7d15ea3075487a48d17412c62b112d7e0cdcc72a269e75d358a75d9af5",
      "create_time": "2022-10-21 10:06:45.955"
    },
    {
      "user_id": 5,
      "username": "steve",
      "password": "d30aa6f4422040cee131efa311c73dd42dd9f2cb6424f23ac9caf403bec2e4289066e846c3df109f612ef2572f95e17f2eddedc36786ba1eb0f50da571ebcac2",
      "create_time": "2022-10-21 10:06:46.099"
    }
  ]
}
```
---

We see that `alice` has a `user_id` of `2` and `bob` has a `user_id` of `3` 

---
To see what the `required parameters` are for the `managers` table, make a request to `/add/managers`

Request:
```jq
https://bartender.hopto.org/add/managers
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [
    {
      "user_id": "INTEGER",
      "first_name": "TEXT",
      "last_name": "TEXT",
      "phone_number": "TEXT",
      "email": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "missing": [
    {
      "user_id": "INTEGER",
      "first_name": "TEXT",
      "last_name": "TEXT",
      "phone_number": "TEXT",
      "email": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "submitted": [
    {}
  ]
}
```
---
#### Adding `alice` to `managers` table:
Arguments:
```rexx
user_id = 2
first_name = Alice
last_name = Alice
phone_number = (302) 555-5555
email = alice@udel.edu
profile_pic = 1.png
```

Request:
```jq
https://bartender.hopto.org/add/managers/user_id/2/first_name/Alice/last_name/Alice/phone_number/(302) 555-5555/email/alice@udel.edu/profile_pic/1.png
```

Response:
```json
{
  "message": "data added to <managers>",
  "manager_id": 1,
  "user_id": "2"
}
```
---
#### Adding `bob` to `managers` table:
Arguments:
```rexx
user_id = 3
first_name = Bob
last_name = Bob
phone_number = (215) 555-5555
email = bob@udel.edu
profile_pic = 2.png
```

Request:
```erlang
https://bartender.hopto.org/add/managers?user_id=3&first_name=Bob&last_name=Bob&phone_number=(215) 555-5555&email=bob@udel.edu&profile_pic=2.png
```

Response:
```json
{
  "message": "data added to <managers>",
  "manager_id": 2,
  "user_id": "3"
}
```

</details>

---

### 4.3 - Adding `anna` and `steve` to `bartenders` table

<details><summary> (click here to expand) </summary>

---
To see what the `required parameters` are for the `bartenders` table, make a request to `/add/bartenders`

Request:
```jq
https://bartender.hopto.org/add/bartenders
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [
    {
      "user_id": "INTEGER",
      "first_name": "TEXT",
      "last_name": "TEXT",
      "address": "TEXT",
      "phone_number": "TEXT",
      "email": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "missing": [
    {
      "user_id": "INTEGER",
      "first_name": "TEXT",
      "last_name": "TEXT",
      "address": "TEXT",
      "phone_number": "TEXT",
      "email": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "submitted": [
    {}
  ]
}
```
---
#### Adding `anna` to `bartenders` table:
Arguments:
```rexx
user_id = 4
first_name = Anna
last_name = Anna
address = 555 N. Chapel St., Newark, DE 19711
phone_number = (555) 555-5555
email = anna@udel.edu
profile_pic = 3.png
```

Request:
```jq
https://bartender.hopto.org/add/bartenders/user_id/4/first_name/Anna/last_name/Anna/address/555 N. Chapel St., Newark, DE 19711/phone_number/(555) 555-5555/email/anna@udel.edu/profile_pic/3.png
```

Response:
```json
{
  "message": "data added to <bartenders>",
  "bartender_id": 1,
  "user_id": "4"
}
```
---
#### Adding `steve` to `bartenders` table:
Arguments:
```rexx
user_id = 5
first_name = Steve
last_name = Steve
address = 555 S. Main St., Newark, DE 19711
phone_number = (610) 555-5555
email = steve@udel.edu
profile_pic = 4.png
```

Request:
```jq
https://bartender.hopto.org/add/bartenders/user_id/5/first_name/Steve/last_name/Steve/address/555 S. Main St., Newark, DE 19711/phone_number/(610) 555-5555/email/steve@udel.edu/profile_pic/4.png
```

Response:
```json
{
  "message": "data added to <bartenders>",
  "bartender_id": 2,
  "user_id": "5"
}
```

</details>

---

### 4.4 - Adding `Iron Hill` and `Deer Park` to `restaurant_profile` and `restaurant_photos` table

<details><summary> (click here to expand) </summary>

---
To see what the `required parameters` are for the `restaurant_profile` table, make a request to `/add/restaurant_profile`

Request:
```jq
https://bartender.hopto.org/add/restaurant_profile
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [
    {
      "manager_id": "INTEGER",
      "restaurant_name": "TEXT",
      "address": "TEXT",
      "bio": "TEXT",
      "phone_number": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "missing": [
    {
      "manager_id": "INTEGER",
      "restaurant_name": "TEXT",
      "address": "TEXT",
      "bio": "TEXT",
      "phone_number": "TEXT",
      "profile_pic": "TEXT"
    }
  ],
  "submitted": [
    {}
  ]
}
```
---
#### Adding `Iron Hill` to `restaurant_profile` table:
> Recall that `alice` with `manager_id` of `1` is the manager of `Iron Hill`

Arguments:
```rexx
manager_id = 1
restaurant_name = Iron Hill Brewery & Restaurant
address = 147 EAST MAIN ST. NEWARK, DE 19711
bio = Craft Beer and Food
phone_number = (302) 266-9000
profile_pic = 5.png
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_profile/manager_id/1/restaurant_name/Iron Hill Brewery & Restaurant/address/147 EAST MAIN ST. NEWARK, DE 19711/bio/Craft Beer and Food/phone_number/(302) 266-9000/profile_pic/5.png
```

Response:
```json
{
  "message": "data added to <restaurant_profile>",
  "restaurant_id": 1,
  "manager_id": "1"
}
```
---
#### Adding `Deer Park` to `restaurant_profile` table:
> Recall that `bob` with `manager_id` of `2` is the manager of `Deer Park`

Arguments:
```rexx
manager_id = 2
restaurant_name = Deer Park Tavern
address = 108 West Main Street, Newark, DE 19711
bio = Good food and spirits!
phone_number = (302) 368-9414
profile_pic = 6.jpeg
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_profile/manager_id/2/restaurant_name/Deer Park Tavern/address/108 West Main Street, Newark, DE 19711/bio/Good food and spirits!/phone_number/(302) 368-9414/profile_pic/6.jpeg
```

Response:
```json
{
  "message": "data added to <restaurant_profile>",
  "restaurant_id": 2,
  "manager_id": "2"
}
```

---
To see what the `required parameters` are for the `restaurant_photos` table, make a request to `/add/restaurant_photos`

Request:
```jq
https://bartender.hopto.org/add/restaurant_photos
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [
    {
      "restaurant_id": "INTEGER",
      "file_name": "TEXT"
    }
  ],
  "missing": [
    {
      "restaurant_id": "INTEGER",
      "file_name": "TEXT"
    }
  ],
  "submitted": [
    {}
  ]
}
```
---
#### Adding `Iron Hill` photos to the `restaurant_photos` table:
Arguments:
```rexx
restaurant_id = 1
file_name = 7.jpeg
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_photos/restaurant_id/1/file_name/7.jpeg
```

Response:
```json
{
  "message": "data added to <restaurant_photos>",
  "photo_id": 1,
  "restaurant_id": "1"
}
```

Arguments:
```rexx
restaurant_id = 1
file_name = 8.jpeg
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_photos/restaurant_id/1/file_name/8.jpeg
```

Response:
```json
{
  "message": "data added to <restaurant_photos>",
  "photo_id": 2,
  "restaurant_id": "1"
}
```
---
#### Adding `Deer Park` photos to the `restaurant_photos` table:
Arguments:
```rexx
restaurant_id = 2
file_name = 9.jpeg
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_photos/restaurant_id/2/file_name/9.jpeg
```

Response:
```json
{
  "message": "data added to <restaurant_photos>",
  "photo_id": 3,
  "restaurant_id": "2"
}
```

Arguments:
```rexx
restaurant_id = 2
file_name = 10.jpeg
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_photos/restaurant_id/2/file_name/10.jpeg
```

Response:
```json
{
  "message": "data added to <restaurant_photos>",
  "photo_id": 4,
  "restaurant_id": "2"
}
```

</details>

---

### 4.5 - Adding `Iron Hill` and `Deer Park` schedules to the `restaurant_schedule` table

<details><summary> (click here to expand) </summary>

---
To see what the `required parameters` are for the `restaurant_schedule` table, make a request to `/add/restaurant_schedule`

Request:
```jq
https://bartender.hopto.org/add/restaurant_schedule
```

Response:
```json
{
  "message": "missing paramaters",
  "required": [
    {
      "restaurant_id": "INTEGER",
      "mon_open": "DATETIME",
      "mon_close": "DATETIME",
      "tue_open": "DATETIME",
      "tue_close": "DATETIME",
      "wed_open": "DATETIME",
      "wed_close": "DATETIME",
      "thu_open": "DATETIME",
      "thu_close": "DATETIME",
      "fri_open": "DATETIME",
      "fri_close": "DATETIME",
      "sat_open": "DATETIME",
      "sat_close": "DATETIME",
      "sun_open": "DATETIME",
      "sun_close": "DATETIME"
    }
  ],
  "missing": [
    {
      "restaurant_id": "INTEGER",
      "mon_open": "DATETIME",
      "mon_close": "DATETIME",
      "tue_open": "DATETIME",
      "tue_close": "DATETIME",
      "wed_open": "DATETIME",
      "wed_close": "DATETIME",
      "thu_open": "DATETIME",
      "thu_close": "DATETIME",
      "fri_open": "DATETIME",
      "fri_close": "DATETIME",
      "sat_open": "DATETIME",
      "sat_close": "DATETIME",
      "sun_open": "DATETIME",
      "sun_close": "DATETIME"
    }
  ],
  "submitted": [
    {}
  ]
}
```
---
#### Adding `Iron Hill` schedule to the `restaurant_schedule` table:
Arguments:
```rexx
restaurant_id = 1
mon_open = 11:30
mon_close = 21:00
tue_open = 11:30
tue_close = 21:00
wed_open = 11:30
wed_close = 22:00
thu_open = 11:30
thu_close = 22:00
fri_open = 11:30
fri_close = 23:00
sat_open = 11:30
sat_close = 23:00
sun_open = 11:30
sun_close = 21:00
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_schedule/restaurant_id/1/mon_open/11:30/mon_close/21:00/tue_open/11:30/tue_close/21:00/wed_open/11:30/wed_close/22:00/thu_open/11:30/thu_close/22:00/fri_open/11:30/fri_close/23:00/sat_open/11:3
0/sat_close/23:00/sun_open/11:30/sun_close/21:00
```

Response:
```json
{
  "message": "data added to <restaurant_schedule>",
  "schedule_id": 1,
  "restaurant_id": "1"
}
```
---
#### Adding `Deer Park` schedule to the `restaurant_schedule` table:
Arguments:
```rexx
restaurant_id = 2
mon_open = 11:30
mon_close = 01:00
tue_open = 11:30
tue_close = 01:00
wed_open = 11:30
wed_close = 01:00
thu_open = 11:30
thu_close = 01:00
fri_open = 11:30
fri_close = 01:00
sat_open = 10:00
sat_close = 01:00
sun_open = 09:00
sun_close = 01:00
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_schedule/restaurant_id/2/mon_open/11:30/mon_close/01:00/tue_open/11:30/tue_close/01:00/wed_open/11:30/wed_close/01:00/thu_open/11:30/thu_close/01:00/fri_open/11:30/fri_close/01:00/sat_open/10:0
0/sat_close/01:00/sun_open/09:00/sun_close/01:00
```

Response:
```json
{
  "message": "data added to <restaurant_schedule>",
  "schedule_id": 2,
  "restaurant_id": "2"
}
```

</details>

### 4.6 - Simulate Restaurant Requests

<details><summary> (click here to expand) </summary>

---
#### First: log out (current user should be: `admin` with `user_id` of `1`)
Request:
```jq
https://bartender.hopto.org/logout
```

Response:
```json
{
  "message": "user logged out",
  "user_id": "1"
}
```
---
#### Log in as `alice` - the manager of `Iron Hill`:
Arguments:
```rexx
username = alice
password = alice
```

POST Request:
```jq
POST(url='https://bartender.hopto.org/login', data={"username": "alice", "password": "alice"})
```

Response:
```json
{
  "message": "user login success",
  "user_id": 2,
  "username": "alice",
  "token": "IXp5ZGc4cVUvS1VKNTUzRy9nOEpBOXc9PT9nQVNWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeWxJYVVMZz09"
}
```
---
#### Verify that the user `alice` with `user_id` of `2` is a `manager`:
Arguments:
```rexx
user_id = 2
```

Request:
```jq
https://bartender.hopto.org/get/managers/user_id/2
```

Response:
```json
{
  "message": "1 manager entry found",
  "data": {
    "manager_id": 1,
    "user_id": 2,
    "first_name": "Alice",
    "last_name": "Alice",
    "phone_number": "(302) 555-5555",
    "email": "alice@udel.edu",
    "profile_pic": "1.png",
    "entry_time": "2022-10-25 20:39:58.215"
  }
}
```
---
#### Confirm that the manager with `maneger_id` of `1` is an `Iron Hill` manager:
Arguments:
```rexx
manager_id = 1
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_profile/manager_id/1
```

Response:
```json
{
  "message": "1 restaurant_profile entry found",
  "data": {
    "restaurant_id": 1,
    "manager_id": 1,
    "restaurant_name": "Iron Hill Brewery & Restaurant",
    "address": "147 EAST MAIN ST. NEWARK, DE 19711",
    "bio": "Craft Beer and Food",
    "phone_number": "(302) 266-9000",
    "profile_pic": "5.png",
    "entry_time": "2022-10-25 23:00:39.921"
  }
}
```
---
### Let's simulate a few `Restaurant Requests` from `Iron Hill`

#### A Thursday Lunch Shift (completed by `anna`):
Arguments:
```rexx
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-20 10:00:00
shift_end = 2022-10-20 14:30:00
status = completed
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-20 10:00:00/shift_end/2022-10-20 14:30:00/status/completed
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 1,
  "restaurant_id": "1"
}
```

#### Simulate `anna` had `snagged` shift:
Arguments:
```rexx
bartender_id = 1
request_id = 1
restaurant_id = 1
shift_start = 2022-10-20 10:00:00
shift_end = 2022-10-20 14:30:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/1/request_id/1/restaurant_id/1/shift_start/2022-10-20 10:00:00/shift_end/2022-10-20 14:30:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": 1,
  "bartender_id": "1",
  "restaurant_id": "1",
  "request_id": "1"
}
```

#### Simulate `anna` had `completed` shift:
Arguments:
```rexx
bartender_id = 1
shift_id = 1
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-20 10:00:00
shift_end = 2022-10-20 14:30:00
clock_in = 2022-10-20 09:45:00
clock_out = 2022-10-20 14:10:00
hours_worked = 4.42
tips = 85.00
total_earnings = 95.30
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/1/shift_id/1/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-20 10:00:00/shift_end/2022-10-20 14:30:00/clock_in/2022-10-20 09:45:00/clock_out/2022-10-20
14:10:00/hours_worked/4.42/tips/85.00/total_earnings/95.30
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": 1,
  "bartender_id": "1",
  "shift_id": "1",
  "restaurant_id": "1"
}
```

#### A Friday Dinner-Close Shift:
Arguments:
```rexx
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-21 16:00:00
shift_end = 2022-10-22 00:30:00
status = completed
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-21 16:00:00/shift_end/2022-10-22 00:30:00/status/completed
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 2,
  "restaurant_id": "1"
}
```

#### Simulate `steve` snagged `shift`:
Arguments:
```rexx
bartender_id = 2
request_id = 2
restaurant_id = 1
shift_start = 2022-10-21 16:00:00
shift_end = 2022-10-22 00:30:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/2/request_id/2/restaurant_id/1/shift_start/2022-10-21 16:00:00/shift_end/2022-10-22 00:30:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": 2,
  "bartender_id": "2",
  "restaurant_id": "1",
  "request_id": "2"
}
```

#### Simulate `steve` had completed `shift`:
Arguments:
```rexx
bartender_id = 2
shift_id = 2
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-21 16:00:00
shift_end = 2022-10-22 00:30:00
clock_in = 2022-10-21 16:05:00
clock_out = 2022-10-22 01:03:00
hours_worked = 8.97
tips = 147.00
total_earnings = 167.90
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/2/shift_id/2/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-21 16:00:00/shift_end/2022-10-22 00:30:00/clock_in/2022-10-21 16:05:00/clock_out/2022-10-22
01:03:00/hours_worked/8.97/tips/147.00/total_earnings/167.90
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": 2,
  "bartender_id": "2",
  "shift_id": "2",
  "restaurant_id": "1"
}
```

#### A Saturday Cocktail Shift:
Arguments:
```rexx
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-29 18:00:00
shift_end = 2022-10-29 23:00:00
status = open
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-29 18:00:00/shift_end/2022-10-29 23:00:00/status/open
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 3,
  "restaurant_id": "1"
}
```
---
#### Now, log out (current user should be: `alice` with `user_id` of `2`)
Request:
```jq
https://bartender.hopto.org/logout
```

Response:
```json
{
  "message": "user logged out",
  "user_id": "2"
}
```
---
#### Log in as `bob` - the manager of `Deer Park`:
POST Request:
```jq
POST(url='https://bartender.hopto.org/login', data={"username": "bob", "password": "bob"})
```

Response:
```json
{
  "message": "user login success",
  "user_id": 3,
  "username": "bob",
  "token": "IUltbWZ4NEROTzhFdTIzZHdUMXF2SUE9PT9nQVNWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFemxJYVVMZz09"
}
```
---
#### Verify that the user `bob` with `user_id` of `3` is a `manager`:
Arguments:
```rexx
user_id = 3
```

Request:
```jq
https://bartender.hopto.org/get/managers/user_id/3
```

Response:
```json
{
  "message": "1 manager entry found",
  "data": {
    "manager_id": 2,
    "user_id": 3,
    "first_name": "Bob",
    "last_name": "Bob",
    "phone_number": "(215) 555-5555",
    "email": "bob@udel.edu",
    "profile_pic": "2.png",
    "entry_time": "2022-10-25 20:44:47.063"
  }
}
```
---
#### Confirm that the manager with `maneger_id` of `2` is an `Deer Park` manager:
Arguments:
```rexx
manager_id = 2
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_profile/manager_id/2
```

Response:
```json
{
  "message": "1 restaurant_profile entry found",
  "data": {
    "restaurant_id": 2,
    "manager_id": 2,
    "restaurant_name": "Deer Park Tavern",
    "address": "108 West Main Street, Newark, DE 19711",
    "bio": "Good food and spirits!",
    "phone_number": "(302) 368-9414",
    "profile_pic": "6.jpeg",
    "entry_time": "2022-10-25 23:16:31.603"
  }
}
```
---
### Let's simulate a few `Restaurant Requests` from `Deer Park`

#### A Sunday Brunch Shift:
Arguments:
```rexx
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-23 08:00:00
shift_end = 2022-10-23 14:00:00
status = closed
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-23 08:00:00/shift_end/2022-10-23 14:00:00/status/closed
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 4,
  "restaurant_id": "2"
}
```

#### Simulate `anna` had `snagged` shift:
Arguments:
```rexx
bartender_id = 1
request_id = 4
restaurant_id = 2
shift_start = 2022-10-23 08:00:00
shift_end = 2022-10-23 14:00:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/1/request_id/4/restaurant_id/2/shift_start/2022-10-23 08:00:00/shift_end/2022-10-23 14:00:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": 3,
  "bartender_id": "1",
  "restaurant_id": "2",
  "request_id": "4"
}
```

#### Simulate `anna` had `completed` shift:
Arguments:
```rexx
bartender_id = 1
shift_id = 3
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-23 08:00:00
shift_end = 2022-10-23 14:00:00
clock_in = 2022-10-23 07:40:00
clock_out = 2022-10-23 15:25:00
hours_worked = 7.75
tips = 165.00
total_earnings = 192.12
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/1/shift_id/3/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-23 08:00:00/shift_end/2022-10-23 14:00:00/clock_in/2022-10-23 07:40:00/clock_out/2022-10-23
15:25:00/hours_worked/7.75/tips/165.00/total_earnings/192.12
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": 3,
  "bartender_id": "1",
  "shift_id": "3",
  "restaurant_id": "2"
}
```

#### A Monday Dinner-Close Shift:
Arguments:
```rexx
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-24 16:00:00
shift_end = 2022-10-25 02:00:00
status = closed
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-24 16:00:00/shift_end/2022-10-25 02:00:00/status/closed
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 5,
  "restaurant_id": "2"
}
```

#### Simulate `steve` snagged `shift`:
Arguments:
```rexx
bartender_id = 2
request_id = 5
restaurant_id = 2
shift_start = 2022-10-24 16:00:00
shift_end = 2022-10-25 02:00:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/2/request_id/5/restaurant_id/2/shift_start/2022-10-24 16:00:00/shift_end/2022-10-25 02:00:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": 4,
  "bartender_id": "2",
  "restaurant_id": "2",
  "request_id": "5"
}
```

#### Simulate `steve` had completed `shift`:
Arguments:
```rexx
bartender_id = 2
shift_id = 4
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-24 16:00:00
shift_end = 2022-10-25 02:00:00
clock_in = 2022-10-24 16:05:00
clock_out = 2022-10-25 02:13:00
hours_worked = 10.13
tips = 108.00
total_earnings = 143.46
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/2/shift_id/4/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-24 16:00:00/shift_end/2022-10-25 02:00:00/clock_in/2022-10-24 16:05:00/clock_out/2022-10-25
02:13:00/hours_worked/10.13/tips/108.00/total_earnings/143.46
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": 4,
  "bartender_id": "2",
  "shift_id": "4",
  "restaurant_id": "2"
}
```

#### A Wednesday Lunch Shift:
Arguments:
```rexx
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-26 10:30:00
shift_end = 2022-10-26 15:00:00
status = open
```

Request:
```jq
https://bartender.hopto.org/add/restaurant_requests/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-26 10:30:00/shift_end/2022-10-26 15:00:00/status/open
```

Response:
```json
{
  "message": "data added to <restaurant_requests>",
  "request_id": 6,
  "restaurant_id": "2"
}
```

</details>

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

### Let's examine all the tables we created and inserted data from the previous workflows
1. Show Tables: `users`, `bartenders`, `managers`, `restaurant_profile`, `restaurant_photos`, `restaurant_schedule`, `restaurant_requests`, `bartender_shifts`, `bartender_wages`
2. Examine the table `bartender_wages` by `tips`, `total_earnings`, `hours_worked`, `etc...`
3. Investigate `bartenders` that were late or early to their shift
4. Find `shifts` that exceed the `requested hours` and group by `restaurant`

---

### 5.1 - Show Active Tables

<details><summary> (click here to expand) </summary>

#### Table: `users`
Request:
```jq
https://bartender.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "a2025bd8b86a53fccf6f42eae008ccbf65dcf6aa55e0e6a477b57c5d74b1e611e5902fe9673d8cddb84896005e125d589e39e258a7fbeb3e7208b866e7746e60", "create_time": "2022-10-19 00:23:52.930"},
    {"user_id": 2, "username": "alice", "password": "b71dab3e13191834f1f0dd53c8b4be30da005ee7eea47ec8673d41c5ee959be34881a9ac99d473bec40b2de489e83694e5e532babbdcfc16c93d137872cffa96", "create_time": "2022-10-21 10:06:45.643"},
    {"user_id": 3, "username": "bob", "password": "7e6c183ddaf351a96fc6541b6ece83ea130c34ff8151a7e219d7bebace3398d685809c999065a54c7c1c785a4ae5b230f247cae5c97b958c7b881c86e81c3e07", "create_time": "2022-10-21 10:06:45.830"},
    {"user_id": 4, "username": "anna", "password": "a0d7bf58601f8f515eb56fb80ec986e49e40eb96572f33abab6ce924c7b3cd0d3cadeb7d15ea3075487a48d17412c62b112d7e0cdcc72a269e75d358a75d9af5", "create_time": "2022-10-21 10:06:45.955"},
    {"user_id": 5, "username": "steve", "password": "d30aa6f4422040cee131efa311c73dd42dd9f2cb6424f23ac9caf403bec2e4289066e846c3df109f612ef2572f95e17f2eddedc36786ba1eb0f50da571ebcac2", "create_time": "2022-10-21 10:06:46.099"},
  ],
}
```
#### Table: `bartenders`
Request:
```jq
https://bartender.hopto.org/get/bartenders
```

Response:
```json
{
  "message": "found 2 bartender entries",
  "data": [
    {"bartender_id": 1, "user_id": 4, "first_name": "Anna", "last_name": "Anna", "address": "555 N. Chapel St., Newark, DE 19711", "phone_number": "(555) 555-5555", "email": "anna@udel.edu", "profile_pic": "3.png", "entry_time": "2022-10-25 20:52:59.861"},
    {"bartender_id": 2, "user_id": 5, "first_name": "Steve", "last_name": "Steve", "address": "555 S. Main St., Newark, DE 19711", "phone_number": "(610) 555-5555", "email": "steve@udel.edu", "profile_pic": "4.png", "entry_time": "2022-10-25 20:54:39.146"},
  ],
}
```
#### Table: `managers`
Request:
```jq
https://bartender.hopto.org/get/managers
```

Response:
```json
{
  "message": "found 2 manager entries",
  "data": [
    {"manager_id": 1, "user_id": 2, "first_name": "Alice", "last_name": "Alice", "phone_number": "(302) 555-5555", "email": "alice@udel.edu", "profile_pic": "1.png", "entry_time": "2022-10-25 20:39:58.215"},
    {"manager_id": 2, "user_id": 3, "first_name": "Bob", "last_name": "Bob", "phone_number": "(215) 555-5555", "email": "bob@udel.edu", "profile_pic": "2.png", "entry_time": "2022-10-25 20:44:47.063"},
  ],
}
```
#### Table: `restaurant_profile`
Request:
```jq
https://bartender.hopto.org/get/restaurant_profile
```

Response:
```json
{
  "message": "found 2 restaurant_profile entries",
  "data": [
    {"restaurant_id": 1, "manager_id": 1, "restaurant_name": "Iron Hill Brewery & Restaurant", "address": "147 EAST MAIN ST. NEWARK, DE 19711", "bio": "Craft Beer and Food", "phone_number": "(302) 266-9000", "profile_pic": "5.png", "entry_time": "2022-10-25 23:00:39.921"},
    {"restaurant_id": 2, "manager_id": 2, "restaurant_name": "Deer Park Tavern", "address": "108 West Main Street, Newark, DE 19711", "bio": "Good food and spirits!", "phone_number": "(302) 368-9414", "profile_pic": "6.jpeg", "entry_time": "2022-10-25 23:16:31.603"},
  ],
}
```
#### Table: `restaurant_photos`
Request:
```jq
https://bartender.hopto.org/get/restaurant_photos
```

Response:
```json
{
  "message": "found 4 restaurant_photo entries",
  "data": [
    {"photo_id": 1, "restaurant_id": 1, "file_name": "7.jpeg", "entry_time": "2022-10-25 23:28:54.850"},
    {"photo_id": 2, "restaurant_id": 1, "file_name": "8.jpeg", "entry_time": "2022-10-25 23:29:01.316"},
    {"photo_id": 3, "restaurant_id": 2, "file_name": "9.jpeg", "entry_time": "2022-10-25 23:30:24.726"},
    {"photo_id": 4, "restaurant_id": 2, "file_name": "10.jpeg", "entry_time": "2022-10-25 23:30:35.574"},
  ],
}
```
#### Table: `restaurant_schedule`
Request:
```jq
https://bartender.hopto.org/get/restaurant_schedule
```

Response:
```json
{
  "message": "found 2 restaurant_schedule entries",
  "data": [
    {"schedule_id": 1, "restaurant_id": 1, "mon_open": "11:30", "mon_close": "21:00", "tue_open": "11:30", "tue_close": "21:00", "wed_open": "11:30", "wed_close": "22:00", "thu_open": "11:30", "thu_close": "22:00", "fri_open": "11:30", "fri_close": "23:00", "sat_open": "11:30", "sat_close": "23:00", "sun_open": "11:30", "sun_close": "21:00", "entry_time": "2022-10-26 06:11:56.158"},
    {"schedule_id": 2, "restaurant_id": 2, "mon_open": "11:30", "mon_close": "01:00", "tue_open": "11:30", "tue_close": "01:00", "wed_open": "11:30", "wed_close": "01:00", "thu_open": "11:30", "thu_close": "01:00", "fri_open": "11:30", "fri_close": "01:00", "sat_open": "10:00", "sat_close": "01:00", "sun_open": "09:00", "sun_close": "01:00", "entry_time": "2022-10-26 06:14:44.158"},
  ],
}
```
#### Table: `restaurant_requests`
Request:
```jq
https://bartender.hopto.org/get/restaurant_requests
```

Response:
```json
{
  "message": "found 6 restaurant_request entries",
  "data": [
    {"request_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "status": "completed", "entry_time": "2022-10-26 08:37:03.649"},
    {"request_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "status": "completed", "entry_time": "2022-10-26 08:37:37.271"},
    {"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "open", "entry_time": "2022-10-26 08:37:55.831"},
    {"request_id": 4, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "status": "closed", "entry_time": "2022-10-26 09:37:41.581"},
    {"request_id": 5, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "status": "closed", "entry_time": "2022-10-26 09:40:46.969"},
    {"request_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "status": "open", "entry_time": "2022-10-26 09:42:25.607"},
  ],
}
```
#### Table: `bartender_shifts`
Arguments:
```rexx

```

Request:
```jq
https://bartender.hopto.org/get/bartender_shifts
```

Response:
```json
{
  "message": "found 4 bartender_shift entries",
  "data": [
    {"shift_id": 1, "bartender_id": 1, "restaurant_id": 1, "request_id": 1, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "entry_time": "2022-10-26 15:52:36.722"},
    {"shift_id": 2, "bartender_id": 2, "restaurant_id": 1, "request_id": 2, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "entry_time": "2022-10-26 15:56:26.438"},
    {"shift_id": 3, "bartender_id": 1, "restaurant_id": 2, "request_id": 4, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "entry_time": "2022-10-26 15:59:05.430"},
    {"shift_id": 4, "bartender_id": 2, "restaurant_id": 2, "request_id": 5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "entry_time": "2022-10-26 16:01:33.182"},
  ],
}
```
#### Table: `bartender_wages`
Arguments:
```rexx

```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages
```

Response:
```json
{
  "message": "found 4 bartender_wage entries",
  "data": [
    {"wage_id": 1, "bartender_id": 1, "shift_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "clock_in": "2022-10-20 09:45:00", "clock_out": "2022-10-20 14:10:00", "hours_worked": 4.42, "tips": 85.0, "total_earnings": 95.3, "entry_time": "2022-10-26 15:54:31.321"},
    {"wage_id": 2, "bartender_id": 2, "shift_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "clock_in": "2022-10-21 16:05:00", "clock_out": "2022-10-22 01:03:00", "hours_worked": 8.97, "tips": 147.0, "total_earnings": 167.9, "entry_time": "2022-10-26 15:57:21.838"},
    {"wage_id": 3, "bartender_id": 1, "shift_id": 3, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "clock_in": "2022-10-23 07:40:00", "clock_out": "2022-10-23 15:25:00", "hours_worked": 7.75, "tips": 165.0, "total_earnings": 192.12, "entry_time": "2022-10-26 16:00:15.348"},
    {"wage_id": 4, "bartender_id": 2, "shift_id": 4, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "clock_in": "2022-10-24 16:05:00", "clock_out": "2022-10-25 02:13:00", "hours_worked": 10.13, "tips": 108.0, "total_earnings": 143.46, "entry_time": "2022-10-26 16:02:35.836"},
  ],
}
```

</details>

---

### 5.2 - Examining the Table `bartender_wages`

<details><summary> (click here to expand) </summary>

#### Filter `bartender_wages` by `bartender_id` (alice == 1):
Arguments:
```rexx
bartender_id = 1
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/bartender_id/1
```

Response:
```json
{
  "message": "found 2 bartender_wage entries",
  "data": [
    {"wage_id": 1, "bartender_id": 1, "shift_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "clock_in": "2022-10-20 09:45:00", "clock_out": "2022-10-20 14:10:00", "hours_worked": 4.42, "tips": 85.0, "total_earnings": 95.3, "entry_time": "2022-10-26 15:54:31.321"},
    {"wage_id": 3, "bartender_id": 1, "shift_id": 3, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "clock_in": "2022-10-23 07:40:00", "clock_out": "2022-10-23 15:25:00", "hours_worked": 7.75, "tips": 165.0, "total_earnings": 192.12, "entry_time": "2022-10-26 16:00:15.348"},
  ],
}
```


#### Filter `bartender_wages` by `restaurant_id` (Iron Hill == 1) and sort by `tips`:
Arguments:
```rexx
filter = (restaurant_id = 1) ORDER BY tips DESC
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(restaurant_id = 1) ORDER BY tips DESC
```

Response:
```json
{
  "message": "found 2 bartender_wage entries",
  "data": [
    {"wage_id": 2, "bartender_id": 2, "shift_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "clock_in": "2022-10-21 16:05:00", "clock_out": "2022-10-22 01:03:00", "hours_worked": 8.97, "tips": 147.0, "total_earnings": 167.9, "entry_time": "2022-10-26 15:57:21.838"},
    {"wage_id": 1, "bartender_id": 1, "shift_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "clock_in": "2022-10-20 09:45:00", "clock_out": "2022-10-20 14:10:00", "hours_worked": 4.42, "tips": 85.0, "total_earnings": 95.3, "entry_time": "2022-10-26 15:54:31.321"},
  ],
}
```


#### Filter `bartender_wages` by `tips < 100.00`:
Arguments:
```rexx
filter = (tips < 100.00)
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(tips < 100.00)
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [
    {"wage_id": 1, "bartender_id": 1, "shift_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "clock_in": "2022-10-20 09:45:00", "clock_out": "2022-10-20 14:10:00", "hours_worked": 4.42, "tips": 85.0, "total_earnings": 95.3, "entry_time": "2022-10-26 15:54:31.321"},
  ],
}
```

#### Filter `bartender_wages` where `hours_worked > 5.0` and `total_earnings < 150.00`
Arguments:
```rexx
filter = (hours_worked > 5.0 AND total_earnings < 150.00)
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(hours_worked > 5.0 AND total_earnings < 150.00)
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [
    {"wage_id": 4, "bartender_id": 2, "shift_id": 4, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "clock_in": "2022-10-24 16:05:00", "clock_out": "2022-10-25 02:13:00", "hours_worked": 10.13, "tips": 108.0, "total_earnings": 143.46, "entry_time": "2022-10-26 16:02:35.836"},
  ],
}
```

</details>

---

### 5.3 - Investigate `bartenders` that were late or early to their shift

<details><summary> (click here to expand) </summary>

#### Filtering `bartenders` that were late to their `shift`:
Arguments:
```rexx
filter = (shift_start < clock_in) GROUP BY bartender_id
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(shift_start < clock_in) GROUP BY bartender_id
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [
    {"wage_id": 2, "bartender_id": 2, "shift_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "clock_in": "2022-10-21 16:05:00", "clock_out": "2022-10-22 01:03:00", "hours_worked": 8.97, "tips": 147.0, "total_earnings": 167.9, "entry_time": "2022-10-26 15:57:21.838"},
  ],
}
```

Bartender `bob` is the only bartender to show up `late` to a shift.

#### Sort by the `largest` time `late`:
Arguments:
```rexx
filter = (shift_start < clock_in)
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(shift_start < clock_in)
```

Response:
```json
{
  "message": "found 2 bartender_wage entries",
  "data": [
    {"wage_id": 2, "bartender_id": 2, "shift_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "clock_in": "2022-10-21 16:05:00", "clock_out": "2022-10-22 01:03:00", "hours_worked": 8.97, "tips": 147.0, "total_earnings": 167.9, "entry_time": "2022-10-26 15:57:21.838"},
    {"wage_id": 4, "bartender_id": 2, "shift_id": 4, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "clock_in": "2022-10-24 16:05:00", "clock_out": "2022-10-25 02:13:00", "hours_worked": 10.13, "tips": 108.0, "total_earnings": 143.46, "entry_time": "2022-10-26 16:02:35.836"},
  ],
}
```

Bartender `bob` is consistantly `5 minutes` late.

#### Filtering `bartenders` that were early to their `shift`, sort by `eariest time`:
Arguments:
```rexx
filter = (shift_start >= clock_in) ORDER BY (strftime('%H:%M', time(strftime('%s', shift_start) - strftime('%s', clock_in), 'unixepoch'))) DESC
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(shift_start >= clock_in) ORDER BY (strftime('%H:%M', time(strftime('%s', shift_start) - strftime('%s', clock_in), 'unixepoch'))) DESC
```

Response:
```json
{
  "message": "found 2 bartender_wage entries",
  "data": [
    {"wage_id": 3, "bartender_id": 1, "shift_id": 3, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "clock_in": "2022-10-23 07:40:00", "clock_out": "2022-10-23 15:25:00", "hours_worked": 7.75, "tips": 165.0, "total_earnings": 192.12, "entry_time": "2022-10-26 16:00:15.348"},
    {"wage_id": 1, "bartender_id": 1, "shift_id": 1, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-20 10:00:00", "shift_end": "2022-10-20 14:30:00", "clock_in": "2022-10-20 09:45:00", "clock_out": "2022-10-20 14:10:00", "hours_worked": 4.42, "tips": 85.0, "total_earnings": 95.3, "entry_time": "2022-10-26 15:54:31.321"},
  ],
}
```

Bartender `alice` is consistantly early.  The earliest was `20 mins`, followed by `15 mins`.

</details>

---

### 5.4 - Bartender `shifts` Exceeding `Requested Hours`

<details><summary> (click here to expand) </summary>

#### Filtering `shifts` exceeding `requested hours`:
Arguments:
```rexx
filter = (strftime('%H:%M', time(strftime('%s', clock_out) - strftime('%s', clock_in), 'unixepoch')) >= strftime('%H:%M', time(strftime('%s', shift_end) - strftime('%s', shift_start), 'unixepoch')))
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/filter/(strftime('%H:%M', time(strftime('%s', clock_out) - strftime('%s', clock_in), 'unixepoch')) >= strftime('%H:%M', time(strftime('%s', shift_end) - strftime('%s', shift_start), 'unixepoch')))
```

Response:
```json
{
  "message": "found 3 bartender_wage entries",
  "data": [
    {"wage_id": 2, "bartender_id": 2, "shift_id": 2, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-21 16:00:00", "shift_end": "2022-10-22 00:30:00", "clock_in": "2022-10-21 16:05:00", "clock_out": "2022-10-22 01:03:00", "hours_worked": 8.97, "tips": 147.0, "total_earnings": 167.9, "entry_time": "2022-10-26 15:57:21.838"},
    {"wage_id": 3, "bartender_id": 1, "shift_id": 3, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-23 08:00:00", "shift_end": "2022-10-23 14:00:00", "clock_in": "2022-10-23 07:40:00", "clock_out": "2022-10-23 15:25:00", "hours_worked": 7.75, "tips": 165.0, "total_earnings": 192.12, "entry_time": "2022-10-26 16:00:15.348"},
    {"wage_id": 4, "bartender_id": 2, "shift_id": 4, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-24 16:00:00", "shift_end": "2022-10-25 02:00:00", "clock_in": "2022-10-24 16:05:00", "clock_out": "2022-10-25 02:13:00", "hours_worked": 10.13, "tips": 108.0, "total_earnings": 143.46, "entry_time": "2022-10-26 16:02:35.836"},
  ],
}
```

There were `3 shifts` that exceeded the `requested hours`

</details>


</details>

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

### Simulate Snagging a `Restaurant Request` and Reporting `Bartender Wages`
1. Help `anna` and `steve` find an `open shift` by snagging a `restaurant request`
2. Simulate the `completion` of a shift by reporting to `bartender_wages`

### Executing Profile Edits and Updating Restaurant Wages
3. `anna` and `steve` would like to edit their `username` to use their `email` and update their `password`
4. `Iron Hill` is increasing the `hourly_wage` from `$2.33` to `$2.50` effective `2022-10-29 00:00:01` 

---

#### 6.1 Simulate Snagging a Restaurant Request

<details><summary> (click here to expand) </summary>

#### Let's have `anna` snag a `restaurant request`

To get available `open` requests, query the `/get` endpoint

Arguments:
```rexx
status = open
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/status/open
```

Response:
```json
{
  "message": "found 2 restaurant_request entries",
  "data": [
    {"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "open", "entry_time": "2022-10-26 08:37:55.831"},
    {"request_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "status": "open", "entry_time": "2022-10-26 09:42:25.607"},
  ],
}
```

There are `2 open requests` available. 

To map the `restaurant_id` with a restaurant profile, query the `restaurant_profile` table.

Arguments:
```rexx
filter = (restaurant_id = 1 or restaurant_id = 2)
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_profile/filter/(restaurant_id = 1 or restaurant_id = 2)
```

Response:
```json
{
  "message": "found 2 restaurant_profile entries",
  "data": [
    {"restaurant_id": 1, "manager_id": 1, "restaurant_name": "Iron Hill Brewery & Restaurant", "address": "147 EAST MAIN ST. NEWARK, DE 19711", "bio": "Craft Beer and Food", "phone_number": "(302) 266-9000", "profile_pic": "5.png", "entry_time": "2022-10-25 23:00:39.921"},
    {"restaurant_id": 2, "manager_id": 2, "restaurant_name": "Deer Park Tavern", "address": "108 West Main Street, Newark, DE 19711", "bio": "Good food and spirits!", "phone_number": "(302) 368-9414", "profile_pic": "6.jpeg", "entry_time": "2022-10-25 23:16:31.603"},
  ],
}
```

`anna` would like to work the dinner shift at `Iron Hill`

#### Snagging a Restaurant Request for `Iron Hill`

#### 1. Change the `status` of the `restaurant_request` from `open` to `snagged`
Arguments:
Arguments:
```rexx
status = snagged
filter = (request_id=3)
```

Request:
```erlang
https://bartender.hopto.org/edit/restaurant_requests/status/snagged?filter=(request_id=3)
```

Response:
```json
{
  "message": "edited 1 restaurant_request entry",
  "submitted": [{"filter": "(request_id=3)", "status": "snagged"}],
}
```
#### Verify the `status` change:
Arguments:
```rexx
request_id = 3
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/request_id/3
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "snagged", "entry_time": "2022-10-26 08:37:55.831"}],
}
```
#### 2. Add the `restaurant_request` to `bartender_shifts`:
Arguments:
```rexx
bartender_id = 1
restaurant_id = 1
request_id = 3
shift_start = 2022-10-29 18:00:00
shift_end = 2022-10-29 23:00:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/1/restaurant_id/1/request_id/3/shift_start/2022-10-29 18:00:00/shift_end/2022-10-29 23:00:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": "5",
  "bartender_id": "1",
  "restaurant_id": "1",
  "request_id": "3",
}
```
#### Verify the `shift` add:
Arguments:
```rexx
request_id = 3
```

Request:
```jq
https://bartender.hopto.org/get/bartender_shifts/request_id/3
```

Response:
```json
{
  "message": "1 bartender_shift entry found",
  "data": [{"shift_id": 5, "bartender_id": 1, "restaurant_id": 1, "request_id": 3, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "entry_time": "2022-10-27 14:30:08.661"}],
}
```

#### Now let's have `steve` snag a `restaurant request`

To get available `open` requests, query the `/get` endpoint

Arguments:
```rexx
status = open
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/status/open
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "status": "open", "entry_time": "2022-10-26 09:42:25.607"}],
}
```

There is `1 open request` available. 

To map the `restaurant_id` with a restaurant profile, query the `restaurant_profile` table.

Arguments:
```rexx
filter = (restaurant_id=2)
```

Request:
```erlang
https://bartender.hopto.org/get/restaurant_profile/?filter=(restaurant_id=2)
```

Response:
```json
{
  "message": "1 restaurant_profile entry found",
  "data": [{"restaurant_id": 2, "manager_id": 2, "restaurant_name": "Deer Park Tavern", "address": "108 West Main Street, Newark, DE 19711", "bio": "Good food and spirits!", "phone_number": "(302) 368-9414", "profile_pic": "6.jpeg", "entry_time": "2022-10-25 23:16:31.603"}],
}
```

#### Snagging a Restaurant Request for `Deer Park`

#### 1. Change the `status` of the `restaurant_request` from `open` to `snagged`
Arguments:
```rexx
status = snagged
filter = (request_id=6)
```

Request:
```erlang
https://bartender.hopto.org/edit/restaurant_requests/status/snagged?filter=(request_id=6)
```

Response:
```json
{
  "message": "edited 1 restaurant_request entry",
  "submitted": [{"filter": "(request_id=6)", "status": "snagged"}],
}
```
#### Verify the `status` change:
Arguments:
```rexx
request_id = 6
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/request_id/6
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "status": "snagged", "entry_time": "2022-10-26 09:42:25.607"}],
}
```

#### 2. Add the `restaurant_request` to `bartender_shifts`:
Arguments:
```rexx
bartender_id = 2
restaurant_id = 2
request_id = 6
shift_start = 2022-10-26 10:30:00
shift_end = 2022-10-26 15:00:00
```

Request:
```jq
https://bartender.hopto.org/add/bartender_shifts/bartender_id/2/restaurant_id/2/request_id/6/shift_start/2022-10-26 10:30:00/shift_end/2022-10-26 15:00:00
```

Response:
```json
{
  "message": "data added to <bartender_shifts>",
  "shift_id": "6",
  "bartender_id": "2",
  "restaurant_id": "2",
  "request_id": "6",
}
```
#### Verify the `shift` add:
Arguments:
```rexx
request_id = 6
```

Request:
```jq
https://bartender.hopto.org/get/bartender_shifts/request_id/6
```

Response:
```json
{
  "message": "1 bartender_shift entry found",
  "data": [{"shift_id": 6, "bartender_id": 2, "restaurant_id": 2, "request_id": 6, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "entry_time": "2022-10-27 14:41:34.785"}],
}
```

</details>

---

#### 6.2 Simulate Completion of a Bartender Shift

<details><summary> (click here to expand) </summary>

#### Anna just finished working her shift!

#### 1. Update the `restaurant_request` from `status=snagged` to `status=completed` 
Arguments:
```rexx
status = completed
filter = (request_id=3)
```

Request:
```erlang
https://bartender.hopto.org/edit/restaurant_requests/status/completed?filter=(request_id=3)
```

Response:
```json
{
  "message": "edited 1 restaurant_request entry",
  "submitted": [{"filter": "(request_id=3)", "status": "completed"}],
}
```

#### Verify `shift` completed:
Arguments:
```rexx
request_id = 3
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/request_id/3
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "completed", "entry_time": "2022-10-26 08:37:55.831"}],
}
```

#### 2. Report the `wages_earned` and `hours_worked` to `bartender_wages`
Arguments:
```rexx
bartender_id = 1
shift_id = 5
restaurant_id = 1
hourly_wage = 2.33
shift_start = 2022-10-29 18:00:00
shift_end = 2022-10-29 23:00:00
clock_in = 2022-10-29 17:50:00
clock_out = 2022-10-29 22:30:00
hours_worked = 4.67
tips = 124.00
total_earnings = 134.88
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/1/shift_id/5/restaurant_id/1/hourly_wage/2.33/shift_start/2022-10-29 18:00:00/shift_end/2022-10-29 23:00:00/clock_in/2022-10-29 17:50:00/clock_out/2022-10-29 22:30:00/hours_worked/4.67/tips/124.00/total_earnings/134.88
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": "5",
  "bartender_id": "1",
  "shift_id": "5",
  "restaurant_id": "1",
}
```
#### Verify the `reporting`:
Arguments:
```rexx
shift_id = 5
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/shift_id/5
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [{"wage_id": 5, "bartender_id": 1, "shift_id": 5, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "clock_in": "2022-10-29 17:50:00", "clock_out": "2022-10-29 22:30:00", "hours_worked": 4.67, "tips": 124.0, "total_earnings": 134.88, "entry_time": "2022-10-27 15:12:05.665"}],
}
```

#### Steve just finished working his shift!

#### Let's update the `restaurant_request` from `status=snagged` to `status=completed` 

#### 1. Update the `restaurant_request` from `status=snagged` to `status=completed`
Arguments:
```rexx
status = completed
filter = (request_id=6)
```

Request:
```erlang
https://bartender.hopto.org/edit/restaurant_requests/status/completed?filter=(request_id=6)
```

Response:
```json
{
  "message": "edited 1 restaurant_request entry",
  "submitted": [{"filter": "(request_id=6)", "status": "completed"}],
}
```
#### Verify `shift` completed:
Arguments:
```rexx
request_id = 6
```

Request:
```jq
https://bartender.hopto.org/get/restaurant_requests/request_id/6
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "status": "completed", "entry_time": "2022-10-26 09:42:25.607"}],
}
```

#### 2. Report the `wages_earned` and `hours_worked` to `bartender_wages`
Arguments:
```rexx
bartender_id = 2
shift_id = 6
restaurant_id = 2
hourly_wage = 3.50
shift_start = 2022-10-26 10:30:00
shift_end = 2022-10-26 15:00:00
clock_in = 2022-10-26 10:15:00
clock_out = 2022-10-26 15:20:00
hours_worked = 5.08
tips = 87.00
total_earnings = 104.78
```

Request:
```jq
https://bartender.hopto.org/add/bartender_wages/bartender_id/2/shift_id/6/restaurant_id/2/hourly_wage/3.50/shift_start/2022-10-26 10:30:00/shift_end/2022-10-26 15:00:00/clock_in/2022-10-26 10:15:00/clock_out/2022-10-26 15:20:00/hours_worked/5.08/tips/87.00/total_earnings/104.78
```

Response:
```json
{
  "message": "data added to <bartender_wages>",
  "wage_id": "6",
  "bartender_id": "2",
  "shift_id": "6",
  "restaurant_id": "2",
}
```
#### Verify the `reporting`:
Arguments:
```rexx
shift_id = 6
```

Request:
```jq
https://bartender.hopto.org/get/bartender_wages/shift_id/6
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [{"wage_id": 6, "bartender_id": 2, "shift_id": 6, "restaurant_id": 2, "hourly_wage": 3.5, "shift_start": "2022-10-26 10:30:00", "shift_end": "2022-10-26 15:00:00", "clock_in": "2022-10-26 10:15:00", "clock_out": "2022-10-26 15:20:00", "hours_worked": 5.08, "tips": 87.0, "total_earnings": 104.78, "entry_time": "2022-10-27 15:16:46.651"}],
}
```

</details>

---

#### 6.3 Making Changes to `username` and `password`

<details><summary> (click here to expand) </summary>

#### Let's start with `anna`

#### `anna` would like to change her `username` from `anna` to `anna@udel.edu` and her `password` from `anna` to `Anna1234`

#### Query the `users` table to see all of the current `users`:
Request:
```jq
https://bartender.hopto.org/get/users
```

Response:
```json
{
  "message": "found 5 user entries",
  "data": [
    {"user_id": 1, "username": "admin", "password": "a2025bd8b86a53fccf6f42eae008ccbf65dcf6aa55e0e6a477b57c5d74b1e611e5902fe9673d8cddb84896005e125d589e39e258a7fbeb3e7208b866e7746e60", "create_time": "2022-10-19 00:23:52.930"},
    {"user_id": 2, "username": "alice", "password": "b71dab3e13191834f1f0dd53c8b4be30da005ee7eea47ec8673d41c5ee959be34881a9ac99d473bec40b2de489e83694e5e532babbdcfc16c93d137872cffa96", "create_time": "2022-10-21 10:06:45.643"},
    {"user_id": 3, "username": "bob", "password": "7e6c183ddaf351a96fc6541b6ece83ea130c34ff8151a7e219d7bebace3398d685809c999065a54c7c1c785a4ae5b230f247cae5c97b958c7b881c86e81c3e07", "create_time": "2022-10-21 10:06:45.830"},
    {"user_id": 4, "username": "anna", "password": "a0d7bf58601f8f515eb56fb80ec986e49e40eb96572f33abab6ce924c7b3cd0d3cadeb7d15ea3075487a48d17412c62b112d7e0cdcc72a269e75d358a75d9af5", "create_time": "2022-10-21 10:06:45.955"},
    {"user_id": 5, "username": "steve", "password": "d30aa6f4422040cee131efa311c73dd42dd9f2cb6424f23ac9caf403bec2e4289066e846c3df109f612ef2572f95e17f2eddedc36786ba1eb0f50da571ebcac2", "create_time": "2022-10-21 10:06:46.099"},
  ],
}
```

#### Changing the `username` and `password` for `anna`:
Arguments:
```rexx
username = anna@udel.edu
password = Anna1234
filter = (user_id=4)
```

Request:
```erlang
https://bartender.hopto.org/edit/users/username/anna@udel.edu/password/Anna1234/?filter=(user_id=4)
```

Response:
```json

{
  "message": "edited 1 user entry",
  "submitted": [
    {
      "filter": "(user_id=4)",
      "username": "anna@udel.edu",
      "password": "ec02990bdcf740a8199c04381671dc07b915f901886c7b54b963e7dbd31fe637aec1d503072c3b8867724589280b477420293430f7c43fcf4bd3d578035dfe2d"
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
POST(url="https://bartender.hopto.org/login", data={"username": "anna@udel.edu", "password": "Anna1234"})
```

Response:
```json

{
  "message": "user login success",
  "user_id": 4,
  "username": "anna@udel.edu",
  "token": "IUd4bkYyTnpGWStUdmJnYlpYcHBqOEE9PT9nQVNWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFMGxJYVVMZz09"
}
```

#### `steve` would like to change his `username` to `steve@gmail.com` and his `password` to `St3ve4321`

#### Changing the `username` and `password` for `steve`:
Arguments:
```rexx
username = steve@gmail.com
password = St3ve4321
filter = (user_id=5)
```

Request:
```erlang
https://bartender.hopto.org/edit/users/username/steve@gmail.com/password/St3ve4321/?filter=(user_id=5)
```

Response:
```json

{
  "message": "edited 1 user entry",
  "submitted": [
    {
      "filter": "(user_id=5)",
      "username": "steve@gmail.com",
      "password": "2a36242977e07c434ebbb9057e004c8748de5332f8a9acd11343900af03c10069ff21c15c6965d5b60d4f31c148dddee179c1af9895d95f872890bbb73adcb27"
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
POST(url="https://bartender.hopto.org/login", data={"username": "steve@gmail.com", "password": "St3ve4321"})
```

Response:
```json

{
  "message": "user login success",
  "user_id": 5,
  "username": "steve@gmail.com",
  "token": "IWVoZEFuTXAxbjlmWmFSWUtmWlAza3c9PT9nQVNWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFMWxJYVVMZz09"
}
```
</details>

---

#### 6.4 `Iron Hill` is increasing the `hourly_wage` from `$2.33` to `$2.50` effective `2022-10-29 00:00:01`

<details><summary> (click here to expand) </summary>

#### The `hourly_wage` parameter exists in the `bartender_wages` and `restaurant_requests` tables

#### Before `editing` a table, let's determine the number of updates we need to make for each table:
Arguments:
```rexx
filter = (restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Request:
```erlang
https://bartender.hopto.org/get/restaurant_requests/?filter=(restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "completed", "entry_time": "2022-10-26 08:37:55.831"}],
}
```

Arguments:
```rexx
filter = (restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Request:
```erlang
https://bartender.hopto.org/get/bartender_wages/?filter=(restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [{"wage_id": 5, "bartender_id": 1, "shift_id": 5, "restaurant_id": 1, "hourly_wage": 2.33, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "clock_in": "2022-10-29 17:50:00", "clock_out": "2022-10-29 22:30:00", "hours_worked": 4.67, "tips": 124.0, "total_earnings": 134.88, "entry_time": "2022-10-27 15:12:05.665"}],
}
```

1 entry for each table needs to be updated

#### Updating the `restaurant_requests` table:

Arguments:
```rexx
hourly_wage = 2.5
filter = (restaurant_id = '1' AND shift_end > '2022-10-29 00:00:01')
```

Request:
```erlang
https://bartender.hopto.org/edit/restaurant_requests/hourly_wage/2.5/?filter=(restaurant_id = '1' AND shift_end > '2022-10-29 00:00:01')
```

Response:
```json
{
  "message": "edited 1 restaurant_request entry",
  "submitted": [{"filter": "(restaurant_id = \"1\" AND shift_end > \"2022-10-29 00:00:01\")", "hourly_wage": "2.5"}],
}
```

#### Updating the `bartender_wages` table:
> Note: We should also update the `total_earning` when updating the `hourly_wage` in this table

Arguments:
```rexx
hourly_wage = 2.50
total_earnings = 135.68
filter = (restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Request:
```erlang
https://bartender.hopto.org/edit/bartender_wages/hourly_wage/2.50/total_earnings/135.68/?filter=(restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Response:
```json
{
  "message": "edited 1 bartender_wage entry",
  "submitted": [{"filter": "(restaurant_id = \"1\" AND shift_end > \"2022-10-29 00:00:01\")", "hourly_wage": "2.50", "total_earnings": "135.68"}],
}
```

#### Verify the changes:
Arguments:
```rexx
filter = (restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Request:
```erlang
https://bartender.hopto.org/get/restaurant_requests/?filter=(restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Response:
```json
{
  "message": "1 restaurant_request entry found",
  "data": [{"request_id": 3, "restaurant_id": 1, "hourly_wage": 2.5, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "status": "completed", "entry_time": "2022-10-26 08:37:55.831"}],
}
```

Arguments:
```rexx
filter = (restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Request:
```erlang
https://bartender.hopto.org/get/bartender_wages/?filter=(restaurant_id = "1" AND shift_end > "2022-10-29 00:00:01")
```

Response:
```json
{
  "message": "1 bartender_wage entry found",
  "data": [{"wage_id": 5, "bartender_id": 1, "shift_id": 5, "restaurant_id": 1, "hourly_wage": 2.5, "shift_start": "2022-10-29 18:00:00", "shift_end": "2022-10-29 23:00:00", "clock_in": "2022-10-29 17:50:00", "clock_out": "2022-10-29 22:30:00", "hours_worked": 4.67, "tips": 124.0, "total_earnings": 135.68, "entry_time": "2022-10-27 15:12:05.665"}],
}
```

</details>


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

### 1. Let's Delete all of the Entries in the `restaurant_photos` table since we didn't use it.
### 2. Then, let's delete the `restaurant_photos` table.

#### Before we delete anything, let's take a quick look at the `restaurant_photos` table:
Request:
```jq
https://bartender.hopto.org/get/restaurant_photos
```

Response:
```json
{
  "message": "found 4 restaurant_photo entries",
  "data": [
    {"photo_id": 1, "restaurant_id": 1, "file_name": "7.jpeg", "entry_time": "2022-10-25 23:28:54.850"},
    {"photo_id": 2, "restaurant_id": 1, "file_name": "8.jpeg", "entry_time": "2022-10-25 23:29:01.316"},
    {"photo_id": 3, "restaurant_id": 2, "file_name": "9.jpeg", "entry_time": "2022-10-25 23:30:24.726"},
    {"photo_id": 4, "restaurant_id": 2, "file_name": "10.jpeg", "entry_time": "2022-10-25 23:30:35.574"},
  ],
}
```

#### 7.1 Deleting all of the Entries in the `restaurant_photos` table:
Arguments:
```rexx
filter = (photo_id > 0)
```

Request:
```erlang
https://bartender.hopto.org/delete/restaurant_photos/?filter=(photo_id > 0)
```

Response:
```json
{
  "message": "4 restaurant_photo entries deleted",
  "submitted": [{"filter": "(photo_id > 0)"}],
}
```

#### Verify the entries have been deleted:
Request:
```jq
https://bartender.hopto.org/get/restaurant_photos
```

Response:
```json
{
  "message": "0 restaurant_photo entries found using submitted parameters",
  "data": [{"submitted": [{}, {"filter": ""}]}],
}
```

#### 7.2 Deleting the `restaurant_photos` table:
Request:
```jq
https://bartender.hopto.org/deleteTable/restaurant_photos
```

Response:
```json
{
  "message": "1 table deleted!",
  "table": "restaurant_photos",
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
https://bartender.hopto.org/uploadImageUrl
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
url = "https://bartender.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png"
```

Request:
```ruby
https://bartender.hopto.org/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png
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
