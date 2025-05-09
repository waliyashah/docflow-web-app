from flask import Blueprint, render_template, session
from routes.decorators import login_required
from db.db_connection import get_connection


# Define a Blueprint for log-related routes
log_bp = Blueprint('log', __name__, template_folder='../templates')

# ------------------------------------------------------
# Route: /log/<in_id>
# Purpose: View the action log for a specific initiative
# Access: Requires login
# ------------------------------------------------------
@log_bp.route('/log/<in_id>')
@login_required
def initiative_log(in_id):

    """
    Displays the full action history (audit trail) of a specific initiative.

    - Queries the ActionLog table for all actions performed on the given IN_ID.
    - Converts the result into a list of dictionaries for easy rendering.
    - Passes the log data to log.html for presentation.
    """

    conn = get_connection()
    cursor = conn.cursor()

    #  Retrieve logs for the selected initiative, ordered by most recent first
    cursor.execute("""
        SELECT Action_Type, Performed_By, Performed_Role, Timestamp
        FROM ActionLog
        WHERE IN_ID = ?
        ORDER BY Timestamp DESC
    """, (in_id,))
    
    # Format result into a list of dictionaries for rendering in Jinja2
    logs = [
        {
            "Action_Type": row[0],
            "Performed_By": row[1],
            "Performed_Role": row[2],
            "Timestamp": row[3]
        }
        for row in cursor.fetchall()
    ]
    # Render the audit log view
    return render_template("log.html", logs=logs, in_id=in_id)
