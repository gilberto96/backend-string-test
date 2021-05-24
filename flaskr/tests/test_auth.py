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
from flask_jwt_extended import create_access_token

def test_login(mocker, app):
    # Arrange
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    user = getMockUsers(1)[0]
    mocker.patch('flaskr.models.user.User.authenticate', return_value = user)   
    client = app.test_client()
    url = "/auth/login"

    # Act
    response =  client.post(url, json = user.to_dict())
    access_token = json.loads(response.get_data())["access_token"]
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert len(access_token) > 0

    
def test_logout(mocker, app):
    # Arrange
    value = getMockUsers(1)[0]
    mocker.patch('flaskr.database.db.session.add', return_value = value) 
    mocker.patch('flaskr.database.db.session.commit', return_value = value) 
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   

    client = app.test_client()
    url = "/auth/logout"

    access_token = ""
    with client.application.app_context():
        access_token = create_access_token(value.to_dict())
    mocker.patch('flask_jwt_extended.get_jwt', return_value = access_token) 

    # Act
    response =  client.delete(url, headers = {
        "Authorization": f"Bearer {access_token}"
    })
    print(response.get_data())
    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["success"] == True