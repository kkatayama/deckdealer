#!/usr/bin/env python3

usage_add = {
    "message": "usage info: '/add'",
    "description": "add a single entry into a table: <table_name>",
    "endpoints": {
        "/add": {
            "returns": "returns all tables[] in the database",
        },
        "/add/usage": {
            "returns": "message: 'usage-info",
        },
        "/add/<table_name>": {
            "returns": "message: 'missing parameters'",
        },
        "/add/<table_name>/<param_name>/<param_value>": {
            "url_paths": "add entry: 'param_name=param_value'",
            "example": "/add/users/username/user_01/password/user_01",
            "response": {
                "message": "data added to {users}",
                "user_id": 8
            },
        },
        "/add/<table_name>?param_name=param_value": {
            "params": "add entry: 'param_name=param_value'",
            "example": "/add/users?username=user_01&password=user_01",
            "response": {
                "message": "data added to {users}",
                "user_id": 8
            },
        },
        "Required": "'user_id' and all params not '*_id' and '*_time'",
        "Exception": "no 'user_id' when adding to the users table",
        "Response": {
            "'user_id'": "when entry added to 'users' table",
            "'<ref>_id'": "when entry added to any other table",
        },
    },
}

usage_get = {
    "message": "usage info: '/get'",
    "description": "fetch entry/entries from a table: <table_name>",
    "endpoints": {
        "/get": {
            "returns": "return all tables[] in the database",
        },
        "/get/usage": {
            "returns": "{'message': 'usage-info'}",
        },
        "/get/<table_name>": {
            "returns": "returns all entries for the table: <table_name>",
        },
        "/get/<table_name>/<param_name>/<param_value>": {
            "url_paths": "match entries: 'param_name=param_value'",
            "example": "/get/users/username/bob",
            "response": {
                "message": "1 user entry found",
                "data": {
                    "user_id": 8, "username": "bob", "password": "8..4", "create_time": "2022-04-05 03:25:57.163"
                },
            },
        },
        "/get/<table_name>?param_name=param_value": {
            "params": "match entries: 'param_name=param_value'",
            "example": "/get/users?user_id=8",
            "response": {
                "message": "1 user entry found",
                "data": {
                    "user_id": 8, "username": "bob", "password": "8..4", "create_time": "2022-04-05 03:25:57.163"
                },
            },
        },
        "/get/<table_name>/filter/query": {
            "url_paths": "match entries: 'filter=[query]'",
            "example": "/get/oximeter/filter/(temperature > '100.4') GROUP BY user_id",
            "response": {
                "message": "1 oximeter entry found",
                "data": {
                    "entry_id": 53, "user_id": 8, "heart_rate": 133, "blood_o2": 95, "temperature": 101.71, "entry_time": "2022-04-05 12:16:54.651"
                },
            },
        },
        "/get/<table_name>?filter=query": {
            "params": "match entries: 'filter=[query]'",
            "example": "/get/users?filter=(create_time > \"2022-04-03\")",
            "response": {
                "message": "found 3 user entries",
                "data": [
                    {"user_id": 6, "username": "M2band", "password": "3..4", "create_time": "2022-04-03 15:29:41.223"},
                    {"user_id": 7, "username": "alice@udel.edu", "password": "d..a", "create_time": "2022-04-05 03:25:57.163"},
                    {"user_id": 8, "username": "robert@udel.edu", "password": "8..4", "create_time": "2022-04-05 03:41:12.857"},
                ],

            },
        },
        "Options": {
            "Parameters": {
                "None": "submit no parameters (none required)",
                "/key/value": "match is limited to 'column_name == column_value'",
                "?key=value": "match is limited to 'column_name == column_value'",
                "/filter/query": "supports expressions, operators, and functions",
                "?filter=query": "supports expressions, operators, and functions",
            }
        },
        "Response": {
            "data": {
                "{object}": "a single object matching the parameters",
                "[{object}]": "a single object matching the parameters"
            }
        },
    },
}



usage_edit = {
    "message": "usage info: '/edit'",
    "description": "edit entry/entries from a table: <table_name>",
    "endpoints": {
        "/edit": {
            "returns": "return all tables[] in the database",
        },
        "/edit/usage": {
            "returns": "message: 'usage-info'",
        },
        "/edit/<table_name>": {
            "returns": "message: 'missing a parameter'",
        },
        "/edit/<table_name>/<param_name>/<param_value>": {
            "url_paths": "edit entries: 'param_name=param_value'",
            "example": "/edit/users/username/robert?user_id=8",
            "response": {
                "message": "edited 1 user entry",
                "submitted": [{"username": "robert", "user_id": "8"}]
            },
        },
        "/edit/<table_name>?param_name=param_value": {
            "params": "edit entries: 'param_name=param_value'",
            "example": "/edit/users/username/robert?user_id=8",
            "response": {
                "message": "edited 1 user entry",
                "submitted": [{"username": "robert", "user_id": "8"}]
            },
        },
        "/edit/<table_name>/filter/query": {
            "url_paths": "edit entries: 'filter=[query]'",
            "example": "/edit/oximeter/temperature/(temperature-32.0)*(5.0/9.0)?filter=(user_id='7')",
            "response": {
                "message": "edited 6 oximeter entries",
                "submitted": [{
                    "filter": "(user_id='7')",
                    "temperature": "((5.0/9.0)*(temperature-32.0))"
                }]
            },
        },
        "/edit/<table_name>?filter=query": {
            "params": "edit entries: 'filter=[query]'",
            "example": "/edit/oximeter/temperature/(temperature-32.0)*(5.0/9.0)?filter=(user_id='7')",
            "response": {
                "message": "edited 6 oximeter entries",
                "submitted": [{
                    "filter": "(user_id='7')",
                    "temperature": "((5.0/9.0)*(temperature-32.0))"
                }]
            },
        },
        "Required": {
            "Parameters": {
                "at least 1 edit parameter": "any parameter not '*_id' or '*_time'",
                "at least 1 reference parameter": "any '*_id' or '*_time' parameter or 'filter'"
                }
        },
        "Response": {
            "message": "number of edits made",
            "submitted[]": "the parameters that were submitted",
        },
    },
}

usage_delete = {
    "message": "usage info: '/delete'",
    "description": "delete entry/entries from a table: <table_name>",
    "endpoints": {
        "/delete": {
            "returns": "return all tables[] in the database",
        },
        "/delete/usage": {
            "returns": "message: 'usage-info'",
        },
        "/delete/<table_name>": {
            "returns": "message: 'missing a parameter'",
        },
        "/delete/<table_name>/<param_name>/<param_value>": {
            "url_paths": "delete entries: 'param_name=param_value'",
            "example": "/delete/oximeter?filter=(user_id = '8' AND temperature > '100.4')",
            "response": {
                "message": "6 oximeter entries deleted",
                "submitted": [{"filter": "(user_id = '8' AND temperature > '100.4')"}]
            },
        },
        "/delete/<table_name>?param_name=param_value": {
            "params": "delete entries: 'param_name=param_value'",
            "example": "/delete/oximeter?filter=(user_id = '8' AND temperature > '100.4')",
            "response": {
                "message": "6 oximeter entries deleted",
                "submitted": [{"filter": "(user_id = '8' AND temperature > '100.4')"}]
            },
        },
        "/delete/<table_name>/filter/query": {
            "url_paths": "delete entries: 'filter=[query]'",
            "example": "/delete/oximeter?filter=(user_id = '8' AND temperature > '100.4')",
            "response": {
                "message": "6 oximeter entries deleted",
                "submitted": [{"filter": "(user_id = '8' AND temperature > '100.4')"}]
            },
        },
        "/delete/<table_name>?filter=query": {
            "params": "delete entries: 'filter=[query]'",
            "example": "/delete/oximeter?filter=(user_id = '8' AND temperature > '100.4')",
            "response": {
                "message": "6 oximeter entries deleted",
                "submitted": [{"filter": "(user_id = '8' AND temperature > '100.4')"}]
            },
        },
        "Required": {
            "Parameters": {
                "at least 1 reference parameter": "any '*_id' or '*_time' parameter or 'filter'"
                }
        },
        "Response": {
            "message": "number of deletes made",
            "submitted[]": "the parameters that were submitted",
        },
    },
}



usage_delete_table = {
    "message": "usage info: /deleteTable",
    "description": "delete a table from the database",
    "end_points": {
        "/deleteTable": {
            "returns": "return all tables[] in the database"
        },
        "/deleteTable/usage": {
            "returns": "message: 'usage-info'",
        },
        "/deleteTable/<table_name>": {
            "action": "delete the table: <table_name>",
            "example": "/deleteTable/steps",
            "response": {
                "message": "1 table deleted!",
                "table": "steps"
            }
        },
        "Required": "<table_name>",
        "Response": {
            "message": "number of deletes made",
            "table": "the name of the table that was deleted",
        },
    },
}

usage_create_table = {
    "message": "usage info: /createTable",
    "description": "create a table and insert it into the database",
    "end_points": {
        "/createTable": {
            "returns": "return all tables[] in the database"
        },
        "/createTable/usage": {
            "returns": "message: 'usage-info'",
        },
        "/createTable/<table_name>": {
            "returns": "message: 'missing parameters'",
        },
        "/createTable/<table_name>/<column_name>/<column_type>": {
            "url_paths": "create columns: 'param_name=param_'",
            "example": "/createTable/steps/step_id/INTEGER/user_id/INTEGER/step_count/INTEGER/latitude/DOUBLE/longitude/DOUBLE/step_time/DATETIME",
            "response": {
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
            },
        },
        "/createTable/<table_name>?column_name=column_type": {
            "params": "create columns: 'param_name=param_value'",
            "example": "/createTable/steps?step_id=INTEGER&user_id=INTEGER&step_count=INTEGER&latitude=DOUBLE&longitude=DOUBLE&step_time=DATETIME",
            "response": {
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
            },
        },
        "Required": {
            "Parameters": {
                "user_id": "INTEGER",
                "{ref}_id": "INTEGER",
                "{ref}_time": "DATETIME",
                "column_name": "lowercase with underscores where appropriate",
                "column_type": "one of 'INTEGER', 'DOUBLE', 'TEXT', 'DATETIME'",
            }
        },
        "Exception": "'{ref}_id' not required when creating 'users' table",
        "Response": {
            "message": "number of tables created",
            "table": "the table name",
            "columns[]": "array of columns with their type"
        },
    },
}

usage_register = {
    "message": "usage info: /register",
    "description": "Register a new user to the [users] table",
    "end_points": {
        "/register": {
            "returns": "missing paramaters",
        },
        "/register/<param_name>/<param_value>": {
            "url_paths": "register with: 'param_name=param_value'",
            "example": "/register/username/admin/password/admin",
            "response": {
                "message": "new user created",
                "user_id": 2,
                "username": "teddy"
            },
        },
        "/register?param_name=param_value": {
            "url_paths": "register with: 'param_name=param_value'",
            "example": "/register?username=teddy&password=teddy&password2=teddy",
            "response": {
                "message": "new user created",
                "user_id": 2,
                "username": "teddy"
            },

        },
        "Required": {
            "Parameters": {
                "username": "TEXT",
                "password": "TEXT",
                "password2": "TEXT"
                }
        },
        "Response": {
            "message": "new user created",
            "user_id": "INTEGER",
            "username": "TEXT",
            "token": "TEXT"
        },
    },
}

usage_login = {
    "message": "usage info: /login",
    "description": "login a user",
    "end_points": {
        "/login": {
            "returns": "message: 'missing parameters'"
        },
        "/login/<param_name>/<param_value>": {
            "url_paths": "login with: 'param_name=param_value'",
            "example": "/login/username/admin/password/admin",
            "response": {
                "message": "user login success",
                "user_id": 1,
                "username": "admin",
                "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
            },
        },
        "/login?param_name=param_value": {
            "params": "login with: 'param_name=param_value'",
            "example": "/login?username=admin&password=admin",
            "response": {
                "message": "user login success",
                "user_id": 1,
                "username": "admin",
                "token": "IVA1WTF3UDhOSHVacm1GUk1DRVVaMFE9PT9nQVdWRVFBQUFBQUFBQUNNQjNWelpYSmZhV1NVakFFeGxJYVVMZz09"
            },
        },
        "Required": {
            "Parameters": {
                "username": "TEXT",
                "password": "TEXT"
                }
        },
        "Response": {
            "message": "user login success",
            "user_id": "INTEGER",
            "username": "TEXT",
            "token": "TEXT"
        },
    },
}

usage_logout = {
    "message": "usage info: /logout",
    "description": "logout a user",
    "end_points": {
        "/logout": {
            "returns": "message: 'user logged out'"
        },
    },

}

usage_uploadImageUrl = {
    "message": "usage info: /uploadImageUrl",
    "description": "upload an image to the backend via image url",
    "end_points": {
        "/uploadImageUrl": {
            "returns": "missing paramaters",
        },
        "/uploadImageUrl/usage": {
            "returns": "message: 'usage-info'",
        },
        "/uploadImageUrl/<param_name>/<param_value>": {
            "url_paths": "upload with: 'param_name=param_value'",
            "example": "/uploadImageUrl/url/https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
            "response": {
                "message": "image url uploaded",
                "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
                "filename": "/static/img/2.png"
            },
        },
        "/uploadImageUrl?param_name=param_value": {
            "url_paths": "upload with: 'param_name=param_value'",
            "example": "/uploadImageUrl?url=https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
            "response": {
                "message": "image url uploaded",
                "url": "https://www.ironhillbrewery.com/assets/craft/TAPHOUSE_LOGO.png",
                "filename": "/static/img/2.png"
            },
        },
        "Required": {
            "Parameters": {
                "url": "TEXT",
                }
        },
        "Response": {
            "message": "image url uploaded",
            "url": "TEXT",
            "filename": "TEXT"
        },
    },
}
