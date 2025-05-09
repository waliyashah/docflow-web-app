from flask import Blueprint, render_template, request, redirect, flash, session
from routes.decorators import login_required, role_required
import json


initiative_bp = Blueprint('initiative', __name__, template_folder='../templates')

# Database connection
from db.db_connection import get_connection

@initiative_bp.route('/add_initiative', methods=['GET', 'POST'])
@login_required
@role_required('Manager', 'Approver')
def add_initiative():

    from flask import session

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':

        role = session.get('role')
        performed_by = session.get('name') or session.get('email')
        
        in_id = request.form['in_id']
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        # status = request.form.get('status')
        year = request.form.get('year')
        division_name = request.form['division_name']
        
       
        if role == 'Approver':
            status = request.form.get('status', 'Approved')
        else:
            status = 'Pending Approval'

        needs_approval = 1 if status == 'Pending Approval' else 0


        # Get Division_ID
        cursor.execute("SELECT Division_ID FROM Division_Table WHERE Division_Name = ?", (division_name,))
        division = cursor.fetchone()
        if not division:
            flash("Division not found.", "danger")
            return redirect('/add_initiative')
        division_id = division[0]

        # Check for duplicate IN_ID
        cursor.execute("SELECT 1 FROM Initiative_Table WHERE IN_ID = ?", (in_id,))
        if cursor.fetchone():
            flash("Initiative ID already exists.", "warning")
            return redirect('/add_initiative')

        # Insert into Initiative_Table
        cursor.execute("""
            INSERT INTO Initiative_Table (IN_ID, Title, Category, Description, Division_ID, Status, Year, Needs_Approval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (in_id, title, category, description, division_id, status, year, needs_approval))

        # Insert into ActionLog
        cursor.execute("""
            INSERT INTO ActionLog (IN_ID, Action_Type, Performed_By, Performed_Role)
            VALUES (?, ?, ?, ?)
        """, (in_id, 'Created' ,performed_by, role))

        # Employees
        emp_ids = request.form.getlist('emp_id')
        emp_names = request.form.getlist('emp_name')
        emp_roles = request.form.getlist('emp_role')

        for emp_id, name, role in zip(emp_ids, emp_names, emp_roles):
            if emp_id.strip() == "":
                continue

            # Insert employee if not exists
            cursor.execute("SELECT 1 FROM Employee_Table WHERE Emp_ID = ?", (emp_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO Employee_Table (Emp_ID, Name, Role)
                    VALUES (?, ?, ?)
                """, (emp_id, name or "Unknown", role or "Not Assigned"))

            # Link in junction table
            cursor.execute("SELECT 1 FROM Employee_Initiative_Table WHERE IN_ID = ? AND Emp_ID = ?", (in_id, emp_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO Employee_Initiative_Table (IN_ID, Emp_ID)
                    VALUES (?, ?)
                """, (in_id, emp_id))

        conn.commit()
        flash("Initiative added successfully!", "success")
        return redirect('/')

    # Load division names
    cursor.execute("SELECT DISTINCT Division_Name FROM Division_Table WHERE Division_Name IS NOT NULL AND Division_Name != ''")
    divisions = [row[0] for row in cursor.fetchall()]

    # Load categories
    cursor.execute("SELECT DISTINCT Category FROM Initiative_Table WHERE Category IS NOT NULL AND Category != ''")
    categories = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT Emp_ID, Name FROM Employee_Table")
    employee_records = [tuple(row) for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Role FROM Employee_Table WHERE Role IS NOT NULL AND Role != ''")
    roles = [row[0] for row in cursor.fetchall()]


    return render_template('add_initiative.html', divisions=divisions, categories=categories, employee_records=employee_records, roles=roles)

