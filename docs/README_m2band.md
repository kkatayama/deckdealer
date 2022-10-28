# Web Framework
[https://m2band.hopto.org](https://m2band.hopto.org)

Framework is loosely modeled after CRUD: [C]reate [R]ead [U]pdate [D]elete

**Features:**
* [*Core Functions*](#Core-Functions) - [**`/add`**](#1-add), [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete)
* [*Admin Functions*](#Admin-Functions) - [**`/createTable`**](#1-createTable) and [**`/deleteTable`**](#2-deleteTable)
* [*User Functions*](User-Functions) - [**`/login`**](#1-login) and [**`/logout`**](#2-logout)
* Query and URL path parameter support
* Additional **filter** parameter - enables SQLite expressions containing operators 
* In-place column editing with SQLite3 expression support
* [**`/get`**](#2-get), [**`/edit`**](#3-edit), [**`/delete`**](4-delete) support single and multiple simultaneous table transactions
* Changes made to the **m2band.db** database are now automatically updated to the GitHub repo in *real-time*

**Design Constrains:**
* All  **`table_names`** and **`column_names`** are defined with **lowercase** letters
* A column name with suffix **`_id`** reference a **unique item** or a **unique item group**.
* A column name with suffix **`_time`** reference a **unique datetime item**
* All tables must have a **`user_id_`** column and a second **`{ref}_id`** `column`
  * The **`users`** table is the only exception and only has one **`{ref}_id`** column: **`user_id`**
* All tables must have one **`{ref}_time`** `column`

**4 Core Functions:**
These functions represent the main endpoints of the framework and will handle the majority of all requests. 
1. [**`/add`**](#1-add) - Add a *single* entry to a `table`
2. [**`/get`**](#2-get) - Fetch a *single* entry or *multiple* entries from a `table`
3. [**`/edit`**](#3-edit) - Edit a *single* entry or *multiple* entries in a `table`
4. [**`/delete`**](#4-delete) - Delete a *single* entry or *multiple* entries from a `table`

**2 Admin Functions**
1. [**`/createTable`**](#1-createTable) - Create a new `table` 
2. [**`/deleteTable`**](#2-deleteTable) - Delete an existing `table`

**2 User Functions**
1. [**`/login`**](#1-login) - Login a user (no signed cookie or token enabled yet)
2. [**`/logout`**](#2-logout) - Logout a user ((no signed cookie or token enabled yet)

---
<details><summary>Debugging Tip!  (click me to expand)
</summary>

To see all of the available `tables` along with the `column_names` and the `column_types`, make a request to the root path of any core or admin function

Request:
```ruby
https://m2band.hopto.org/add
https://m2band.hopto.org/get
https://m2band.hopto.org/edit
https://m2band.hopto.org/delete
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
</details>

---

# Core Functions
The examples listed below will cover the **4 core functions**
All examples shown are executed via a **GET** request and can be tested with any browser.
All endpoints support 4  *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

# 1. `/add`
**Add a *single* entry to a `table`**

### Endpoints:
| Resource | Description  |
|:--|:--|
| **`/add`**  | returns all tables[] in the database |
| **`/add/usage`**  | returns message: 'usage info' |
| **`/add/{table_name}`**  | returns message: 'missing parameters' |
| **`/add/{table_name}/{param_name}/{param_value}`**  | add entry: 'param_name=param_value' |
| **`/add/{table_name}?param_name=param_value`**  | add entry: 'param_name=param_value' |

### Requirements:x
| Parameters | Exception  |
|:--|:--|
| `user_id` and all params not **`*_id`** or **`*_time`** | no `user_id` when adding to **`users`** table |

### Response After Successful [`/add`](#1-add):
| Variable | Comment |
|:--|:--|
| `user_id` | when entry added to **`users`** table |
| `{ref}_id` | when entry added to any other table |  

Note: <br />
> The old functions `/addUser` and `/addSensorData` still work but are kept for backward compatibility. <br />
> `/addUser` has migrated to: `/add/users` <br />
> `/addSensorData` has migrated to: `/add/oximeter` <br />
> It is recommended to update the existing *mp32* and *swift* code to follow the new format

## Workflow Example:
* [Let's add 2 users to the **`users`** table: `alice` and `bob`](#adding-alice-to-the-users-table)
* [Then, add sensor data to the **`oximeter`** table for both users](#adding-sensor-data-for-the-user-alice-to-the-oximeter-table)

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

### Investigating the Endpoint: `/add`
The endpoint for adding a user to the **`users`** is **`/add/users`**.
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

Now that we have added users and sensor data, let's take a look at the next **core function**: [**`/get`**](#2-get)
</details>

---

# 2. `/get`
**Fetch a *single* entry or *multiple* entries from a `table`**

### Endpoints:
| resource | description  |
|:--|:--|
| **`/get`** | returns all tables[] in the database |
| **`/get/usage`** | returns a message for how to use this function |
| **`/get/{table_name}`** | returns all entries for the table: `{table_name}` |
| **`/get/{table_name}/{param_name}/{param_value}`** | match entries: 'param_name=param_value' |
| **`/get/{table_name}?param_name=param_value`**  | match entries: 'param_name=param_value' |
| **`/get/{table_name}/filter/{query}`**  | match entries: 'filter=[query]' |
| **`/get/{table_name}?filter=query`**  | match entries: 'filter=[query]' |

### Options:
| Parameters | Comment  |
|:--|:--|
| *None* | submit no parameters (none required) |
| /key/value | match is limited to 'column_name == column_value' |
| ?key=value | match is limited to 'column_name == column_value' |
| /filter/query | supports **expressions**, **operators**,  and **functions** | 
| ?filter=query | supports **expressions**, **operators**,  and **functions** | 

### Response After Successful [`/get`](#2-get):
| Variable | Comment |
|:--|:--|
| `data = {obj}` | a single object matching the parameters |
| `data = [{obj}]` | an array of objects matching the parameters |

Note:
> The old functions `/getUser`, `/getUsers`, `/getSensorData`, and `/getAllSensorData` still work but are kept for backward compatibility. <br />
> `/getUser` has migrated to: `/get/users` <br />
> `/getUsers` has migrated to: `/get/users` <br />
> `/getSensorData` has migrated to: `/get/oximeter` <br />
> `/getAllSensorData` has migrated to: `/get/oximeter` <br />
> It is recommended to update the existing *mp32* and *swift* code to follow the new format

## Workflow Example:
* [Let's query the **`users`** table to find the 2 users we created earlier](#lets-try-out-the-filter-parameter-to-get-just-the-users-alice-and-bob)
* [Next, we will query the **`oximeter`** table to retrieve the sensor data for each user](#get-sensor-data-for-alice-and-bob)
* Finally, we will examine the **`filter`** parameter and test out a few **test cases**
  * [Test Case](#test-case-fever): Determine which user possibly has a **fever**
  * [Test Case](#test-case-min-max-temperature-range): What was the range of **`temperature`** for this user? **min**? **max**?
  * [Test Case](#test-case-filter-users-created-after-a-start-date-but-before-an-end-date): Filter users created after a *start date* but before an *end date*.

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

### Investigating the Endpoint: `/get`
The endpoint for getting users from the **`users`** table is **`/get/users`**.

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

### Notes on {filter_string}:
| Note | Comment |
|:--|:--|
| keyword | **`filter`** |
| QUERY FORMAT | ?filter=(param_name > "param_value") |
| QUERY EXAMPLE | **`/get/users?filter=(user_id = "7" OR username="bob")`** |
| PATH FORMAT | /filter/(param_name="param_value" OR param_name="param_value") |
| PATH EXAMPLE | /get/users/filter/(username="bob" OR username="alice") |
* the **`param_name`** must never be wrapped in quotations as it is treated as a **variable**
* the **`"param_value"`** is usually wrapped in **"single"** or **"double"** quotations.
  * **NUMBERS** do not have to be wrapped in quotations
* spaces are allowed within an *expression*
                
### `/get` sensor data for `alice` and `bob`

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

# 3. `/edit`
**Edit a single entry or multiple entries of a table**

### Endpoints:
| Resource | Description  |
|:--|:--|
| **`/edit`** | returns all tables[] in the database |
| **`/edit/usage`** | returns message: 'usage-info' |
| **`/edit/{table_name}`** | returns message: 'missing a parameter' |
| **`/edit/{table_name}/{param_name}/{param_value}`** | edit entries: 'param_name=param_value' |
| **`/edit/{table_name}?param_name=param_value`**  | edit entries: 'param_name=param_value' |
| **`/edit/{table_name}/filter/{filter_string}`**  | edit entries: filter=[query]' |
| **`/edit/{table_name}?filter=filter_string`**  | edit entries: filter=[query]' |

### Requirements:
| Parameters | Comment  |
|:--|:--|
| at least 1 edit parameter | any parameter not **`*_id`** or **`*_time`** |
| at least 1 reference parameter | any **`*_id`** or **`*_time`** parameter or **`filter`** |

### Response After Successful [`/edit`](#3-edit):
| Variable | Comment |
|:--|:--|
| `message` | number of edits made |
| `submitted[]` | the parameters that were submitted |

Note:
> The old functions `/editUser` and `/editSensorData` still work but are kept for backward compatibility.
> `/editUser` has migrated to: `/edit/users`
> `/editSensorData` has migrated to: `/edit/oximeter`
> It is recommended to update the existing *mp32* and *swift* code to follow the new format

## Workflow Example:
* [Let's edit bob's **`username`** from `bob` to `robert`](#get-sensor-data-for-alice-and-bob) 
* [Then append `@gmail.com` to the **`username`** for both `robert` and `alice`](#appending-gmailcom-to-the-username-for-both-robert-and-alice)
* Robert and Alice now want their **`username`** to have `@udel.edu`
  * [Let's replace any **`username`** containing `@gmail.com` with `@udel.edu`](#replacing-all-users-with-username-containing-gmailcom-to-udeledu)
* Alice would like her **`temperature`** data to be in celsius
  * [Let's convert the **`temperature`** from **`farenheight`** to **`celsius`**](#converting-the-temperature-from-farenheight-to-celsius-for-alice)

---
<details><summary>Show Workflow Example (click here to expand)
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

# 4. `/delete`
**Delete a single entry or multiple entries of a table**

### Endpoints:
| Resource | Description  |
|:--|:--|
| **`/delete`** | returns all tables[] in the database |
| **`/delete/usage`** | returns message: 'usage-info' |
| **`/delete/{table_name}`** | returns message: 'missing a parameter' |
| **`/delete/{table_name}/{param_name}/{param_value}`** | delete entries: 'param_name=param_value' |
| **`/delete/{table_name}?param_name=param_value`**  | delete entries: 'param_name=param_value' |
| **`/delete/{table_name}/filter/{filter_string}`**  | delete entries: filter=[query]' |
| **`/delete/{table_name}?filter=filter_string`**  | delete entries: filter=[query]' |

### Requirements:
| Parameters | Comment  |
|:--|:--|
| at least 1 reference parameter | any **`*_id`** or **`*_time`** parameter or **`filter`** |

### Response After Successful [`/delete`](#4-delete):
| Variable | Comment |
|:--|:--|
| `message` | number of deletes made |
| `submitted[]` | the parameters that were submitted |


Note:
> The old functions `/deleteUser` and `/deleteSensorData` still work but are kept for backward compatibility.
> `/deleteUser` has migrated to: `/delete/users`
> `/deleteSensorData` has migrated to: `/delete/oximeter`
> It is recommended to update the existing *mp32* and *swift* code to follow the new format

## Workflow Example:
* Robert wasn't too happy that we were able to detect that he had a fever
  * [Let's delete all entries for `Robert` with **`temperature`** in the fever range](#deleting-all-entries-for-robert-with-temperature-in-the-fever-range)

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

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

# Admin Functions
The examples listed below will cover the **2 admin functions**.
All examples shown are executed via a **GET** request and can be tested with any browser.
All endpoints support 4  *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

# 1. `/createTable`
**Create a new `table`**

### Endpoints:
| Resource | Description  |
|:--|:--|
| **`/createTable`**  | returns a list of all existing tables in the database |
| **`/createTable/usage`**  | returns a message for how to use this function |
| **`/createTable/{table_name}`**  | DEBUG: returns the required parameters |
| **`/createTable/{table_name}/{column_name}/{column_type}`**  | create a table with columns using path parameters |
| **`/createTable/{table_name}?column_name=column_type`**  | create a table with columns using query parameters |

### Requirements:
| Parameters | Value  |
|:--|:--|
| user_id | INTEGER |
| {ref}_id | INTEGER |
| {ref}_time | DATETIME |
| column_name | lowercase with underscores where appropriate |
| column_type | one of `INTEGER`, `DOUBLE`, `TEXT`, `DATETIME` |
| Exception | "{ref}_id" not required when creating "users" table |

## Workflow Example:
* Let's create a table named **`steps`** <br /> 
  with the columns **`["step_id", "user_id", "step_count", "latitude", "longitude", "step_time"]`**

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

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
step_id = INTEGER
user_id = INTEGER
step_count = INTEGER
latitude = DOUBLE
longitude = DOUBLE
step_time = DATETIME
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
</details>

---

# 2. `/deleteTable`
**Delete `table`**

### Endpoints:
| Resource | Description |
|:--|:--|
| **`/deleteTable`**  | returns a list of all existing tables in the database |
| **`/deleteTable/usage`**  | returns a message for how to use this function |
| **`/deleteTable/{table_name}`**  | DEBUG: returns the required parameters |

### Requirements:
| Parameters | Description |
|:--|:--|
| table_name | the name of the **`table`** you wish to delete  |

## Workflow Example:
* Let's delete the table named **`steps`** 

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

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
 
# User Functions
The examples listed below will cover the **2 user functions**.
All examples shown are executed via a **GET** request and can be tested with any browser.
All endpoints support 4  *HTTP_METHODS*: **GET**, **POST**, **PUT**, **DELETE**

# 1. `/login`
**Login `user`**

### Endpoints:
| Resource | Description |
|:--|:--|
| **`/login`**  | |
| **`/login/param_name/param_value`**  | login with: 'param_name=param_value' |
| **`/login/param_name=param_value`**  | login with: 'param_name=param_value' |

### Requirements:
| Parameters | Description |
|:--|:--|
| username | the user's username |
| password | the user's password |

## Workflow Example:
* Let's login the user **`alice`** 

---
<details><summary>Show Workflow Example (click here to expand)
</summary>

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
username = alice
```

Request:
```ruby
/login/username/alice@udel.edu
```

Response:
```json
{
    "message": "missing parameters",
    "required": [{"username": "TEXT", "password": "TEXT"}],
    "submitted": [{"username": "alice@udel.edu"}]
}
```

### Let's Login the user `alice`
Arguments:
```python
username = alice@udel.edu
password = alice
```

Request:
```ruby
/login/username/alice@udel.edu/password/alice
```

Response:
```json
{
    "message": "user login success", "user_id": 7, "username": "alice@udel.edu"
}
```
</details>

---

# 2. `/logout`
**Log out a `user`**

### Endpoints:
| Resource | Description |
|:--|:--|
| **`/logout`**  | log out a user |

### Example `/logout`
Request:
```ruby
/logout
```

Response:
```json
{
    'message': 'user logged out'
}
```
