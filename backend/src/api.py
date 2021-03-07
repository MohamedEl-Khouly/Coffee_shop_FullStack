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


# Helper Methods
# 1. get_recipe
'''
    get_recipe

    Inputs:
        - body: The JSON body of the request
    Outputs:
        - recipe: A list of dictionaries describing
                  each component of the recipe.
    Description:
        A private helper method used in post and 
        patch routes to format the recipe item of the
        object before submitting in the DataBase
    Errors expected:
        - Status code 422
'''


def get_recipe(body):
    recipe = []
    recipe_body = body['recipe']
    recipe_type = type(recipe_body)
    if recipe_type == list:
        for element in recipe_body:
            recipe.append({
                'color': element['color'],
                'name': element['name'],
                'parts': element['parts']
            })
    elif recipe_type == dict:
        recipe.append({
            'color': recipe_body['color'],
            'name': recipe_body['name'],
            'parts': recipe_body['parts']
        })
    else:
        abort(422)
    return recipe


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


# 2. GET Drinks-detail
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
@requires_auth(permission='get:drinks-detail')
def drink_recipe(jwt):
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


# 3. POST Drinks
'''
    POST /drinks

    Description:
        A private endpoint that requires
        the 'post:drinks' permission.
        It calls the method create_drink.
        Method create_drink validates the drink
        data , creates a new Object and commits
        it to the DataBase. The method returns
        the newly created drink currently in the long format.
    Output:
        - Status code : 200
        - json response :
            {
                "success" : True,
                "drinks"  : drink_formated,
            }
        - In case of failure expect status code 400,422
'''


@app.route("/drinks", methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drink(jwt):
    # read the json data form body request
    body = request.get_json()
    # check all parts are available
    if not('title' in body and 'recipe' in body):
        abort(400)
    # read data and commit
    try:
        title = body['title']
        recipe = get_recipe(body)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        abort(422)


# 3. PATCH Drinks
'''
    PATCH /drinks/<id>

    Description:
        A private endpoint that requires
        the 'patch:drinks' permission and 
        an id that is available in DataBase.
        It calls the method edit_drink.
        Method edit_drink validates the body
        of the request , retrives the data corresponding
        to the id from the database, updates it and commits
        it to the DataBase. The method returns
        the updated drink in the long format.
    Output:
        - Status code : 200
        - json response :
            {
                "success" : True,
                "drinks"  : drink_formated,
            }
        - In case of failure expect status code 401, 403, 400, 422
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def edit_drink(jwt, drink_id):
    # query for drink
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    # check if drink found
    if drink is None:
        abort(404)
    # read request body
    body = request.get_json()
    # check body data
    if ('title' in body or 'recipe' in body):
        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            recipe = get_recipe(body)
            drink.recipe = json.dumps(recipe)
    else:
        abort(422)
    # commit to database
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


# 5. DELETE Drink
'''
    DELETE /drinks/<id>

    Description:
        A private endpoint that requires
        the 'delete:drinks' permission and 
        an id that is available in DataBase.
        It calls the method remove_drink.
        Method remove_drink validates the body
        of the request , retrives the data corresponding
        to the id from the database, deletes it and commits
        it to the DataBase. The method returns the deleted drink id.
    Output:
        - Status code : 200
        - json response :
            {
                "success" : True,
                "delete"  : drink_id,
            }
        - In case of failure expect status code 401, 403, 404
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def remove_drink(jwt, drink_id):
    # query for drink
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    # check if drink found
    if drink is None:
        abort(404)
    # delete drink
    drink.delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    })


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
