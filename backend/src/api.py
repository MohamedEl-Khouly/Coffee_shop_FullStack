import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
# 1. GET Drinks
'''
    GET /drinks

    Description:
        A public endpoint that calls the method get_drinks.
        Method get_drinks returns  a list of
        all drinks currently available in the database.
    Output:
        - Status code : 200
        - json response :
            {
                "success" : True,
                "drinks"  : drinks_formated,
            }
        - In case of failure expect status code 404
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    # Query all drinks stored in Database
    drinks = Drink.query.order_by(Drink.id).all()
    # Check if query result is empty
    if len(drinks) == 0:
        abort(404)
    # format drinks to short format
    drinks_formated = [drink.short() for drink in drinks]
    # format json response
    return jsonify({
        "success": True,
        "drinks": drinks_formated,
    })


# 2. GET Drinks
'''
    GET /drinks-detail

    Description:
        A private endpoint that requires 
        the 'get:drinks-detail' permission.
        It calls the method drink_recipe.
        Method drink_recipe returns  a list of
        all drinks currently available in the database
        in the long format.
    Output:
        - Status code : 200
        - json response :
            {
                "success" : True,
                "drinks"  : drinks_formated,
            }
        - In case of failure expect status code 404
'''


@app.route('/drinks-detail', methods=['GET'])
def drink_recipe():
    # Query all drinks stored in Database
    drinks = Drink.query.order_by(Drink.id).all()
    # Check if query result is empty
    if len(drinks) == 0:
        abort(404)
    # format drinks to long format
    drinks_formated = [drink.long() for drink in drinks]
    # format json response
    return jsonify({
        "success": True,
        "drinks": drinks_formated,
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
    Error Handlers
        For each error the error handlers compose
        a suitable JSON respone that describe that error.

    Response format
        {
            "success" : False,
            "error" : status code,
            "message" : error description
        } 
'''


# 1. Error 422
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "UNPROCESSABLE Request"
    }), 422


# 2. Error 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


# 3. Error 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


# 4. Auth Error
@app.errorhandler(AuthError)
def authentication_failed(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        "description": error.error['description'],
    }), error.status_code
