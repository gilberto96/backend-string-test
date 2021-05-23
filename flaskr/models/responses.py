from sqlalchemy_serializer import SerializerMixin

class ApiResponse(SerializerMixin):
    def __init__(self, code, success, message = ""):
        self.code = code
        self.success = success
        self.message = message

    def toJson(self):
        return {
            "code": self.code,
            "success": self.success,
            "message": self.message
        }