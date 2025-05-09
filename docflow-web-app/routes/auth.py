from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash
from models.user_model import get_user_by_email_or_name


# Define a Blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# -----------------------------------------------
# Route: /login
# Methods: GET, POST
# -----------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    """
    Handles user login.

    - Accepts email or name as input.
    - Validates the password using hashed check.
    - If credentials are valid, stores user info in session.
    - Redirects to home page on success or shows error on failure.
    """

    if request.method == 'POST':

        # Get user input from form, normalize whitespace and lowercase
        user_input = request.form.get('user_input', '').strip().lower()
        password = request.form.get('password', '')

        # Retrieve user record using flexible match (email or name)
        user = get_user_by_email_or_name(user_input)

        # Verify credentials using hashed password comparison
        if user and check_password_hash(user['hashpassword'], password):
            # Store essential user info in session
            session['user_id'] = user['id']
            session['username'] = user['name']
            session['name'] = user['name'] 
            session['email'] = user['email']
            session['role'] = user['role']
            
            # Redirect to homepage after successful login
            return redirect(url_for('home'))
        else:

             # Show error if login fails
            flash("Invalid credentials", "danger")

    # Render login form on GET or after failed POST
    return render_template("login.html")

# -----------------------------------------------
# Route: /logout
# Method: GET
# -----------------------------------------------
@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session and redirecting to the login page.
    """
    session.clear()  # Remove all user data from session
    return redirect(url_for('auth.login'))  # Redirect to login page
