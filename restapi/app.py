import os
import sys
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gaenv'))

from google.appengine.ext import db
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import InvalidParamsError
import models

app = Flask('t8-restapi-py')
app.debug = True
app.config.from_object('restapi.settings')
jsonrpc = JSONRPC(app, '/restaurant/0.1/', enable_web_browsable_api=True)

RESTAURANT_UID = "@test-mcdonalds"


@jsonrpc.method('System.Test(Test=str) -> Object')
def System_Test(Test=None):
    """ INTERNAL CALL: Some general system tests, checking/showing how errors and other conditions are handled """
    if not Test:
        raise InvalidParamsError()
    if Test == 'fatal':
        x = 1 / 0
    return {}


@jsonrpc.method('System.CreateTestData(CleanupOnly=bool) -> Object')
def System_CreateTestData(CleanupOnly=None):
    """ Deletes/Creates data for the unit-tests """
    REGION_UIDS_TO_DELETE = ["@test-san-francisco", "@test-los-angeles"]
    RESTAURANT_UIDS_TO_DELETE = ["@test-mcdonalds", "@test-In-N-Out", "@test-Wendys"]
    TAGS_UIDS_TO_DELETE = ["@test-american", "@test-french"]

    db.delete([x for x in models.Region.all().filter("Uid IN", REGION_UIDS_TO_DELETE)])
    db.delete([x for x in models.Restaurant.all().filter("Uid IN", RESTAURANT_UIDS_TO_DELETE)])
    db.delete([x for x in models.RestaurantTag.all().filter("Uid IN", TAGS_UIDS_TO_DELETE)])

    if not CleanupOnly:
        region1 = models.Region(Uid="@test-san-francisco", Title="TEST San Francisco"); region1.put()
        region2 = models.Region(Uid="@test-los-angeles", Title="TEST Los Angeles"); region2.put()
        resturant1 = models.Restaurant(Uid="@test-mcdonalds", Title="TEST McDonalds", Description="TEST Description McDonalds", Tags=["French Cuisine"], Regions=[region1.Uid]); resturant1.put()
        resturant2 = models.Restaurant(Uid="@test-In-N-Out", Title="TEST In-N-Out", Description="TEST Description In-N-Out", Tags=["French Cuisine", "American"], Regions=[region2.Uid]); resturant2.put()
        resturant3 = models.Restaurant(Uid="@test-Wendys", Title="TEST Wendys", Description="TEST Description Wendys", Tags=["American"], Regions=[region1.Uid, region2.Uid]); resturant3.put()
        logging.warn([resturant1])
        pass
    return {}


@jsonrpc.method('Region.Retrieve() -> Object')
def Region_Retrieve():
    """ Returns the complete region list """
    items = [models.to_dict(x) for x in models.Region.all()]
    response = {}
    response['Count'] = len(items)
    response['Items'] = items
    return response


@jsonrpc.method('RestaurantTag.Retrieve() -> Object')
def RestaurantTag_Retrieve():
    """ Returns the complete list of tags that can be used for restaurants """
    items = [models.to_dict(x) for x in models.RestaurantTag.all()]
    response = {}
    response['Count'] = len(items)
    response['Items'] = items
    return {}


@jsonrpc.method('RestaurantDetail.Retrieve() -> Object')
def RestaurantDetail_Retrieve():
    """ Returns the restaurant details """

    restaurant = None
    for restaurant in models.Restaurant.all().filter("Uid =", RESTAURANT_UID):
        break
    assert restaurant, 'The expected restaurant record %r does not exists? It should\'ve been created already' % RESTAURANT_UID
    response = {}
    response['Count'] = 1
    response['Items'] = [models.to_dict(restaurant)]
    return response


@jsonrpc.method('RestaurantDetail.Update(Title=str, Details=str, Tags=list, Regions=list) -> Object')
def RestaurantDetail_Update(Title=None, Details=None, Tags=None, Regions=None):
    """ Updates the restaurant details """
    RESTAURANT_UID = "@test-mcdonalds"
    restaurant = None
    for restaurant in models.Restaurant.all().filter("Uid =", RESTAURANT_UID):
        break
    assert restaurant, 'The expected restaurant record %r does not exists? It should\'ve been created already' % RESTAURANT_UID
    if Title is not None:
        restaurant.Title = Title
    if Details is not None:
        restaurant.Details = Details
    if Tags is not None:
        restaurant.Tags = Tags
    if Regions is not None:
        restaurant.Regions = Regions
    restaurant.put()
    response = {}
    response['Count'] = 1
    response['Items'] = [models.to_dict(restaurant)]
    return response
