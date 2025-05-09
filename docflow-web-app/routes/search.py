from flask import Blueprint, render_template, request, session
from models.initiative_model import search_initiatives, get_report_count_by_initiative
from routes.decorators import login_required

#Create a search blueprints
search_bp = Blueprint("search", __name__)

# Initialize the search route
# This route handles the search functionality and filters initiatives based on user input.
@search_bp.route('/search')
@login_required
def search():

    # Use getlist to capture multiple selections
    selected_divisions = request.args.getlist("division")

    #Collect filter parameters from query string; default to 'all' if not provided
    filter_options = {
        "category": request.args.get("category", "all"),
        "division": selected_divisions if selected_divisions else ["all"],
        "status": request.args.get("status", "all"),
        "year": request.args.get("year", "all"),
        "search_query": request.args.get("search_query", "").strip()  # Combine text searches
    }

        
     # # Call the search function and get filtered initiatives; always return a list
    initiatives = search_initiatives(filter_options) or []  # Ensure it's always a list

    # ✅ Add ReportCount to each initiative
    for i in initiatives:
        i['ReportCount'] = get_report_count_by_initiative(i['IN_ID'])


    # Handle case where no results are found
    message = None if initiatives else "No matching initiatives found."

    # Determine if the logged-in user is an Approver (used to control what the UI shows)
    role = session.get('role')
    user_is_approver = (role == 'Approver')


    # Render the results template with the filtered initiatives and message
    return render_template("results.html", initiatives=initiatives, message=message, user_is_approver=user_is_approver)


