from flaskr.utils import compare
from flaskr.tests.mock import getMockResponseApi, getMockUsers, getMockUsersWithTasks
from flask import Flask
from werkzeug.wrappers import response
from flaskr.blueprints import schedule
from flaskr.models.user import User
import json
from unittest.mock import MagicMock
from flask_sqlalchemy import SQLAlchemy
import pytest

def test_get_users(mocker, app):
    # Arrange
    data_length = 5
    mocker.patch('flaskr.models.user.User.get_all', return_value = getMockUsers(data_length))   
    client = app.test_client()
    url = "/security/users"

    # Act
    response =  client.get(url)

    # Asserts
    assert response.content_type == "application/json"
    assert len(json.loads(response.get_data())) == data_length
    assert type(json.loads(response.get_data())) == list
    assert response

def test_get_user(mocker, app):
    # Arrange
    value = getMockUsers(1)[0]
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = value) 
    client = app.test_client()
    url = f"/security/users/{value.id}"

    # Act
    response =  client.get(url)

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["id"] == value.id
    assert response

def test_post_user(mocker, app):
    # Arrange
    value = getMockUsers(1)[0]
    mocker.patch('flaskr.models.user.User.save', return_value = value) 
    client = app.test_client()
    url = "/security/users"

    # Act
    response =  client.post(url, json = value.to_dict())

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == value.id


def test_update_user(mocker, app):
    # Arrange
    value = getMockUsers(1)[0]
    mocker.patch('flaskr.models.user.User.save', return_value = value) 
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = value) 
    client = app.test_client()
    url = "/security/users"

    # Act
    response =  client.put(url, json = value.to_dict())

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == value.id


def test_delete_user(mocker, app):
    # Arrange
    value = getMockUsers(1)[0]
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = value) 
    mocker.patch('flaskr.models.user.User.delete', return_value = True) 
    client = app.test_client()
    url = "/security/users/1"

    # Act
    response =  client.delete(url)
    
    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == value.id


def test_delete_user_with_tasks(mocker, app):
    # Arrange
    value = getMockUsersWithTasks(1)[0]
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = value) 
    mocker.patch('flaskr.models.user.User.delete', return_value = True) 
    client = app.test_client()
    url = "/security/users/1"

    # Act
    response =  client.delete(url)
    
    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert response.status_code == 400
    assert json.loads(response.get_data())["code"] == 0

    
def test_delete_user_not_exist(mocker, app):
    # Arrange
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = None) 
    mocker.patch('flaskr.models.user.User.delete', return_value = True) 
    client = app.test_client()
    url = "/security/users/1"

    # Act
    response =  client.delete(url)
    
    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert response.status_code == 404
    assert json.loads(response.get_data())["code"] == 0