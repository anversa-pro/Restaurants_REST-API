from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt import jwt_required

from config import db
from models.city import City
from models.country import Country
from models.restaurant import Restaurant
from validators.validator import Validator

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__, url_prefix="/restaurants")


@restaurant_blueprint.route('/create', methods=['POST'])
@jwt_required()
@swag_from('../documentation/create_restaurant.yml')
def create_restaurant():
    try:
        body_json = request.json

        name = body_json.get('name') or ''
        ranking = body_json.get('ranking') or ''
        chef = body_json.get('chef') or ''
        abstract = body_json.get('abstract') or ''
        access = body_json.get('public_access') or False
        city = body_json.get('city') or ''
        user_id = request.userid

        create = Validator.validate_nonempty(name, ranking, chef, abstract, access, city, user_id)

        if create:
            new_restaurant = Restaurant(name=name, ranking=ranking, chef=chef, abstract=abstract, public_access=access,
                                        city=city, user_id=user_id)

            db.session.add(new_restaurant)
            db.session.commit()

            return {'message': f'restaurant {new_restaurant.id} has been created successfully'}, 202

        else:
            return {'message': 'some parameters are missing'}, 400
    except Exception as e:
        print(f'error en create_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/')
@jwt_required()
@swag_from('../documentation/get_restaurants.yml')
def get_restaurants():
    try:
        args = request.args
        page = 1
        per_page = 5

        if args:
            try:
                page = int(args.get('page'))
                per_page = int(args.get('limit'))

                if (page < 0) or (per_page < 0):
                    return {'message': 'sorry, invalid pagination query arguments  :v'}, 400

            except Exception as e:
                print(f'error en get_page(): {e}')
                return {'message': 'sorry, invalid pagination query arguments  :v'}, 400

        restaurants = Restaurant.query.filter_by(public_access=True).paginate(per_page=per_page,
                                                                              page=page, error_out=False)

        if restaurants:
            restaurants_list = []

            pagination = {'total restaurants': restaurants.total,
                          'total pages': restaurants.pages,
                          'current page': restaurants.page,
                          'next page available': restaurants.has_next,
                          'restaurants per page': restaurants.per_page}

            for each in restaurants.items:
                restaurant_dict = each.to_json()
                location = {'city id': each.city, 'city name': each.city_name, 'country id': each.city_two.country,
                            'country name': each.city_two.country_name}
                restaurant_dict.pop('city', 'user_id')
                restaurant_dict['location'] = location
                restaurants_list.append(restaurant_dict)
            return {'pagination': [pagination], 'restaurants': restaurants_list}, 200

        return {'message': 'sorry, we have no restaurants to visit :v'}, 404

    except Exception as e:
        print(f'error en get_restaurants(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/user')
@jwt_required()
@swag_from('../documentation/get_user_restaurants.yml')
def get_user_restaurants():
    user_id = request.userid

    try:
        args = request.args
        private = args.get('private')
        public = args.get('public')
        page = args.get('page')
        per_page = args.get('limit')

        if page or per_page:
            try:
                page = int(page)
                per_page = int(per_page)
                if (page < 0) or (per_page < 0):
                    return {'message': 'sorry, invalid pagination query arguments :v'}, 400
            except Exception as e:
                print(f'error en get_page(): {e}')
                return {'message': 'sorry, invalid pagination query arguments :v'}, 400
        else:
            page = 1
            per_page = 5

        if private:
            try:
                restaurants = Restaurant.query.filter_by(public_access=False,
                                                         user_id=user_id).paginate(per_page=per_page,
                                                                                   page=page, error_out=False)
            except Exception as e:
                print(f'error en get_user_restaurant() private: {e}')
                return {'message': 'sorry, you have no private registers :v'}, 400

        elif public:
            try:
                restaurants = Restaurant.query.filter_by(public_access=True,
                                                         user_id=user_id).paginate(per_page=per_page, page=page,
                                                                                   error_out=False)
            except Exception as e:
                print(f'error en get_user_restaurant() private: {e}')
                return {'message': 'sorry, you have no public registers :v'}, 400

        else:
            restaurants = Restaurant.query.filter_by(user_id=user_id).paginate(per_page=per_page,
                                                                               page=page, error_out=False)

        if restaurants:
            restaurants_list = []

            pagination = {'total restaurants': restaurants.total,
                          'total pages': restaurants.pages,
                          'current page': restaurants.page,
                          'next page available': restaurants.has_next,
                          'restaurants per page': restaurants.per_page}

            for each in restaurants.items:
                restaurant_dict = each.to_json()
                location = {'city id': each.city, 'city name': each.city_name, 'country id': each.city_two.country,
                            'country name': each.city_two.country_name}
                restaurant_dict.pop('city')
                restaurant_dict['location'] = location
                restaurants_list.append(restaurant_dict)
            return {'pagination': [pagination], 'restaurants': restaurants_list}, 200

        return {'message': 'sorry, you have no restaurants to visit :v'}, 404

    except Exception as e:
        print(f'error en get_restaurants(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>')
@jwt_required()
@swag_from('../documentation/get_restaurant_by_id.yml')
def get_restaurant(restaurant_id=None):
    try:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            if restaurant.public_access or request.userid == restaurant.user_id:
                json_result = {'restaurant': restaurant.to_json()}
                json_result['restaurant']['city_name'] = restaurant.city_name
                json_result['restaurant']['country_name'] = restaurant.city_two.country_name
                return json_result, 200
            return {'message': 'sorry, you are not the owner :v'}, 403
        else:
            return {'message': 'sorry, that restaurant does not exist :v'}, 404
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>/update', methods=['PUT'])
@jwt_required()
@swag_from('../documentation/update_restaurant.yml')
def update_restaurant(restaurant_id=None):
    try:
        body_json = request.json
        for key, value in body_json.items():
            if hasattr(Restaurant, key) is False:
                return {"message": f'sorry the attribute: {key}, does not exist '}, 400
        if Restaurant.query.get(restaurant_id):
            Restaurant.query.filter_by(id=restaurant_id).update(body_json)
            db.session.commit()
            return {'message': 'success'}, 200
        return {'message': 'sorry, invalid id'}, 400
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>/delete', methods=['DELETE'])
@jwt_required()
@swag_from('../documentation/delete_restaurant.yml')
def delete_restaurant(restaurant_id=None):
    try:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {'message': 'success'}, 200
        return {'message': 'sorry, invalid id'}, 400
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
