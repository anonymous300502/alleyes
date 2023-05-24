from functools import wraps
from flask import session, redirect, url_for

# define a decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
