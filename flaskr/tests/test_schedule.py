from flaskr.models.tokenblocklist import TokenBlockList
from flaskr.utils import compare
from flaskr.tests.mock import getMockResponseApi, getMockTasks, getMockUsers, getMockUsersWithTasks
from flask import Flask
from werkzeug.wrappers import response
from flaskr.blueprints import schedule
from flaskr.models.user import User
import json
from unittest.mock import MagicMock
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, verify_jwt_in_request

def test_get_tasks(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.user.User.get_by_id', return_value = user)   

    client = app.test_client()
    url = "/schedule/tasks"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())

    # Act
    response =  client.get(url, headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert len(json.loads(response.get_data())) == len(user.tasks)
    assert type(json.loads(response.get_data())) == list
    assert response


def test_get_task(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    task = getMockTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.task.Task.get_single', return_value = task)   

    client = app.test_client()
    url = f"/schedule/tasks/{task.id}"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())

    # Act
    response =  client.get(url, headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["id"] == task.id
    assert response


def test_post_task(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    task = getMockTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.task.Task.save', return_value = task)   

    client = app.test_client()
    url = f"/schedule/tasks/"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())
 
    # Act
    response =  client.post(url,json=task.to_dict(), headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == task.id
    assert response


def test_delete_task(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    task = getMockTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.task.Task.delete', return_value = True)   
    mocker.patch('flaskr.models.task.Task.get_single', return_value = task)   

    client = app.test_client()
    url = f"/schedule/tasks/{task.id}"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())
 
    # Act
    response =  client.delete(url, headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == task.id


def test_delere_task_not_exist(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    task = getMockTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.task.Task.delete', return_value = True)   
    mocker.patch('flaskr.models.task.Task.get_single', return_value = None)   

    client = app.test_client()
    url = f"/schedule/tasks/{task.id}"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())
 
    # Act
    response =  client.delete(url, headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert response.status_code == 404
    assert json.loads(response.get_data())["code"] == 0


def test_update_task(mocker, app):
    # Arrange
    user = getMockUsersWithTasks(1)[0]
    task = getMockTasks(1)[0]
    mocker.patch('flaskr.models.tokenblocklist.TokenBlockList.get_by_token', return_value = None)   
    mocker.patch('flaskr.models.task.Task.get_single', return_value = task)   
    mocker.patch('flaskr.models.task.Task.save', return_value = task)   

    client = app.test_client()
    url = f"/schedule/tasks/"
    app.config["JWT_SECRET_KEY"] = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config["ENV"] = "development"

    access_token = ""

    with client.application.app_context():
        access_token = create_access_token(user.to_dict())
 
    # Act
    response =  client.post(url,json=task.to_dict(), headers = {
        "Authorization": f"Bearer {access_token}"
    })

    # Asserts
    assert response.content_type == "application/json"
    assert type(json.loads(response.get_data())) == dict
    assert json.loads(response.get_data())["code"] == task.id
    assert response
