from functools import wraps
from flask import session, redirect, url_for, flash , render_template

# --------------------------------------------
# Decorator: login_required
# --------------------------------------------
# This decorator checks if the user is logged in.
# If not, it redirects them to the login page with a flash message.
def login_required(f):

    """
    Ensures that the user is logged in before accessing the route.

    - Checks if 'user_id' exists in session.
    - If not present, redirects to login page with a flash warning.
    - Otherwise, allows access to the requested route.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue", "warning")

            # Redirect to login route in auth blueprint
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return wrapped

# --------------------------------------------
# Decorator: role_required
# --------------------------------------------

def role_required(*roles):

    """
    Restricts access to a route based on user roles.

    Parameters:
    - *roles: one or more roles allowed to access the route (e.g., 'Manager', 'Approver')

    Logic:
    - Checks if the current user's role (stored in session) is in the allowed roles list.
    - If unauthorized, displays an "Access denied" message and renders a 403 error page.
    - Otherwise, proceeds with the original route function.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session.get('role') not in roles:
                flash("Access denied", "danger")
                

                 # Show custom unauthorized page
                return render_template("unauthorized.html"), 403

            return f(*args, **kwargs)
        return wrapped
    return decorator
