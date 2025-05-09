from flask import Flask, render_template, redirect, url_for, request , session
from config import Config
from models.initiative_model import get_filter_options 
from models.initiative_model import  get_reports_by_initiative
from models.initiative_model import get_all_reports
from routes.decorators import login_required
from db.db_connection import get_connection

#Initialize the Flask app and load configuration
app = Flask(__name__)
app.config.from_object(Config)


# --------------------------------------
# Registering Blueprints for modular routing
# --------------------------------------

from routes.search import search_bp
app.register_blueprint(search_bp)

from routes.initiative import initiative_bp
app.register_blueprint(initiative_bp)

from routes.update_initiative import update_initiative_bp
app.register_blueprint(update_initiative_bp)

from routes.auth import auth_bp
app.register_blueprint(auth_bp)

from routes.approval import approval_bp
app.register_blueprint(approval_bp)

from routes.log import log_bp
app.register_blueprint(log_bp)

# --------------------------------------
# Routes
# --------------------------------------

# Redirect root to login
@app.route('/')
def root():
    return redirect(url_for('auth.login'))

# Redirect to login page if user is not logged in
@app.route('/index')
@login_required
def home():
    """
    Loads the homepage and fetches dropdown options for filtering.
    """
    dropdown_options = get_filter_options()  # Fetch categories, divisions, statuses, years
    reviewed_updates = []

    
    # Check if the user is a Manager and fetch their reviewed initiatives
    if session.get('role') == 'Manager':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.IN_ID, i.Title, i.Status, a.Action_Type, a.Timestamp
            FROM ActionLog a
            INNER JOIN Initiative_Table i ON a.IN_ID = i.IN_ID
            WHERE a.Performed_By = ? 
              AND a.Action_Type IN ('Approved', 'Rejected')
              AND i.Needs_Approval = 0
            ORDER BY a.Timestamp DESC
        """, (session.get('name'),))
        reviewed_updates = cursor.fetchall()

    return render_template("index.html",
                           dropdown_options=dropdown_options,
                           manager_reviewed_initiatives=reviewed_updates)
    
# Fetch the filter options for categories, divisions, statuses, and years
@app.route('/filter')
@login_required
def filter_page():
    """
    Loads the filter page with dropdown options.
    """
    dropdown_options = get_filter_options()  # Fetch categories, divisions, statuses, years
    return render_template('filters.html', dropdown_options=dropdown_options)

# Fetch the number of reports for a given initiative by IN_ID
@app.route('/initiative/<string:in_id>/reports')
@login_required  # ensure only logged-in users can access
def view_initiative_reports(in_id):
    """
    Route to display all reports for a given initiative.
    """
    # Fetch reports for the initiative using the model
    reports = get_reports_by_initiative(in_id)
   
    # Render the reports view template, passing the initiative ID and its reports list
    return render_template('view_reports.html', in_id=in_id, reports=reports)

# Fetch all reports from the Report_Table
@app.route('/reports/all')
@login_required
def view_all_reports():
    reports = get_all_reports()
    return render_template('view_reports.html', in_id="All", reports=reports)

# Render a 403 error page for unauthorized access
@app.route('/unauthorized')
def unauthorized():
    """
    Renders an unauthorized access page.
    """
    return render_template("unauthorized.html"), 403


# --------------------------------------
# Context Processor
# Injects pending approval count globally into all templates
# --------------------------------------
@app.context_processor
def inject_pending_count():


    """
    Calculates the number of initiatives pending approval.
    This is made available globally in templates for notifications.
    """

    role = session.get('role')
    pending_count = 0

    if role in ['Manager', 'Approver']:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Initiative_Table WHERE Needs_Approval = 1 AND Status = 'Pending Approval'")
        pending_count = cursor.fetchone()[0]

    return dict(pending_count=pending_count)

# Application entry point
if __name__ == "__main__":
    app.run(debug=True)


