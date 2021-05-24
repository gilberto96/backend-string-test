from flaskr.models.task import Task
from flaskr.models.user import User
from flaskr.models.responses import ApiResponse
from datetime import datetime

def getMockUsers(i):
    users = []
    for a in range(1, i+1):
        users.append(User(id = a, email=f"email{a}@gmail.com", password="12341234", fullname = f"Name {a}", photo = f"Photo {a}", created_at = datetime.now()))
    return users


def getMockUsersWithTasks(i):
    users = []
    for a in range(1, i+1):
        users.append(User(id = a, email=f"email{a}@gmail.com", password="12341234", fullname = f"Name {a}", photo = f"Photo {a}", created_at = datetime.now(), tasks = getMockTasks(a)))
    return users

def getMockResponseApi(code, success, message):
    return ApiResponse(code, success, message)


def getMockTasks(i):
    users = []
    for a in range(1, i+1):
        users.append(Task(id = a, title=f"Title {a}", description=f"Description {a}", start_date = f"2021-05-24 10:00:00", due_date = f"2021-05-25 10:00:00", priority=5, created_at = datetime.now()))
    return users