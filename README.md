# APIDiscord

```
pip install -r requirements.txt
python3 API.py
```

// 20210407190328
// http://127.0.0.1:5000/apispec_1.json

{
  "definitions": {
    
  },
  "info": {
    "description": "powered by Flasgger",
    "termsOfService": "/tos",
    "title": "A swagger API",
    "version": "0.0.1"
  },
  "paths": {
    "/achievements": {
      "get": {
        "responses": {
          "200": {
            "description": "All achievements"
          }
        },
        "summary": "Return all achievements "
      }
    },
    "/ranking/{ranking_type}": {
      "get": {
        "parameters": [
          {
            "description": "Type of ranking wanted",
            "in": "path",
            "name": "ranking_type",
            "required": true,
            "schema": {
              "example": "bystander_victory",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "All users"
          }
        },
        "summary": "Return the ranking of the users"
      }
    },
    "/user": {
      "get": {
        "responses": {
          "200": {
            "description": "All users",
            "examples": null,
            "schema": null
          }
        },
        "summary": "Return all users"
      }
    },
    "/user/": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": true,
            "schema": {
              "properties": {
                "u_id": {
                  "example": "208662022160777216",
                  "type": "string"
                },
                "username": {
                  "description": "The user username in Discord",
                  "example": "kekun#2126",
                  "type": "string"
                }
              },
              "required": [
                "u_id",
                "username"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "User successfully added",
            "schema": null
          }
        },
        "summary": "Post a new user"
      }
    },
    "/user/{u_id}": {
      "get": {
        "parameters": [
          {
            "description": "User id",
            "in": "path",
            "name": "u_id",
            "required": true,
            "schema": {
              "example": "208662022160777216",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "A user",
            "schema": {
              "properties": {
                "bystander_victory": {
                  "type": "number"
                },
                "u_id": {
                  "type": "string"
                },
                "undercover_victory": {
                  "type": "number"
                },
                "username": {
                  "type": "string"
                }
              },
              "type": "object"
            }
          }
        },
        "summary": "Get the user ith the specified id"
      }
    },
    "/user/{u_id}/achievements": {
      "get": {
        "parameters": [
          {
            "description": "User id",
            "in": "path",
            "name": "u_id",
            "required": true,
            "schema": {
              "example": "208662022160777216",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "All achievements"
          }
        },
        "summary": "Return all achievements of a user"
      }
    },
    "/user/{u_id}/achievements/": {
      "post": {
        "parameters": [
          {
            "description": "User",
            "in": "path",
            "name": "u_id",
            "required": true,
            "schema": {
              "example": "208662022160777216",
              "type": "string"
            }
          },
          {
            "in": "body",
            "name": "body",
            "required": true,
            "schema": {
              "properties": {
                "a_id": {
                  "description": "Achievement_id",
                  "example": 1,
                  "type": "number"
                }
              },
              "required": [
                "a_id"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Achievement successfully added"
          }
        },
        "summary": "Grant an achievement to the specified user"
      }
    },
    "/user/{u_id}/win": {
      "put": {
        "parameters": [
          {
            "description": "User id",
            "in": "path",
            "name": "u_id",
            "required": true,
            "schema": {
              "example": "208662022160777216",
              "type": "string"
            }
          },
          {
            "in": "body",
            "name": "body",
            "required": true,
            "schema": {
              "properties": {
                "win_type": {
                  "description": "Achievement_id",
                  "example": "undercover_victory",
                  "type": "string"
                }
              },
              "required": [
                "win_type"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Victory successfully added"
          }
        },
        "summary": "Grant a win to the specified user"
      }
    },
    "/wordpair": {
      "get": {
        "responses": {
          "200": {
            "description": "A pair of words",
            "schema": {
              "properties": {
                "bystander_word": {
                  "type": "string"
                },
                "undercover_word": {
                  "type": "string"
                }
              },
              "type": "object"
            }
          }
        },
        "summary": "Return a random WordPair from the database"
      }
    }
  },
  "swagger": "2.0"
}
