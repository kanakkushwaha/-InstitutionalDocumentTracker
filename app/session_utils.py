from flask import session

from app.models import User


def get_session_user():
    user_session = session.get("user") or {}
    user_id = user_session.get("id")

    if user_id:
        user = User.query.get(user_id)
        if user:
            return user

    email = user_session.get("email")
    if email:
        user = User.query.filter_by(email=email, is_active=True).first()
        if user:
            session["user"] = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            }
            return user

    return None
