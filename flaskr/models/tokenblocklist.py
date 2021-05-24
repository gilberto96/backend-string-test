from ..database import db;

class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def get_by_token(token):
        return TokenBlockList.query.filter_by(jti=token).first()
