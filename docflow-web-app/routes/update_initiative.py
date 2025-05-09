from flask import Blueprint, request, render_template, redirect, flash , session
from db.db_connection import get_connection
from routes.decorators import login_required, role_required

#Register the update_initiative blueprint
update_initiative_bp = Blueprint('update_initiative', __name__)

# Initialize the update_initiative route
@update_initiative_bp.route('/update_initiative/<int:id>', methods=['GET', 'POST'])
@login_required

# Only Managers and Approvers can access this route
@role_required('Manager', 'Approver')

def update_initiative(id):
    conn = get_connection()
    cursor = conn.cursor()

    # POST: Update initiative and employees
    if request.method == 'POST':
        try:
            # Get the current user's role and name/email from the session
            role = session.get('role')
            performed_by = session.get('name') or session.get('email')

            # Capture form input
            in_id = request.form['in_id']
            title = request.form['title']
            category = request.form['category']
            description = request.form['description']
            status = request.form.get('status', 'Pending Approval') #fixed default to 'Pending Approval'
            year = request.form.get('year')
            division_name = request.form['division_name']
            

            # Validate required fields
            if role == 'Approver':
                status = request.form.get('status', 'Approved')
            else:
                status = 'Pending Approval'

            # Flag record for approval if edited by a Manager
            needs_approval = 1 if status == 'Pending Approval' else 0


            # Get Division_ID
            cursor.execute("SELECT Division_ID FROM Division_Table WHERE Division_Name = ?", (division_name,))
            division = cursor.fetchone()
            division_id = division[0] if division else None

            # Update initiative table
            cursor.execute("""
                UPDATE Initiative_Table
                SET IN_ID = ?, Title = ?, Category = ?, Description = ?, Status = ?, Year = ?, Division_ID = ?, Needs_Approval = ?
                WHERE ID = ?
            """, (in_id, title, category, description, status, year, division_id, needs_approval, id))


            # Remove previous employee links
            cursor.execute("DELETE FROM Employee_Initiative_Table WHERE IN_ID = ?", (in_id,))

            # Handle employees: First removes all previous links between this initiative and employees.
            emp_ids = request.form.getlist('emp_id')
            emp_names = request.form.getlist('emp_name')
            emp_roles = request.form.getlist('emp_role')


            #Captures submitted employee details (multiple entries supported).
            for emp_id, name, role in zip(emp_ids, emp_names, emp_roles):
                if emp_id.strip() == "":
                    continue

                # Update if exists, else insert
                cursor.execute("SELECT 1 FROM Employee_Table WHERE Emp_ID = ?", (emp_id,))
                if cursor.fetchone():
                    cursor.execute("UPDATE Employee_Table SET Name = ?, Role = ? WHERE Emp_ID = ?", (name, role, emp_id))
                else:
                    cursor.execute("INSERT INTO Employee_Table (Emp_ID, Name, Role) VALUES (?, ?, ?)", 
                                   (emp_id, name or "Unknown", role or "Not Assigned"))

                # Insert relationship: Link employee to initiative
                cursor.execute("INSERT INTO Employee_Initiative_Table (IN_ID, Emp_ID) VALUES (?, ?)", (in_id, emp_id))

               # Insert into ActionLog: Log the action performed by the user
            cursor.execute("""
                INSERT INTO ActionLog (IN_ID, Action_Type, Performed_By, Performed_Role)
                VALUES (?, ?, ?, ?)
            """, (in_id, 'Edited',performed_by, role))   


            conn.commit()
            flash("Initiative updated successfully!", "success") # message to be displayed on the page
            return redirect(f'/update_initiative/{id}')
        
        except Exception as e:

            conn.rollback()
            flash(f"Update failed: {str(e)}", "danger") # message to be displayed on the page
            return redirect(f'/update_initiative/{id}')

    # GET: Fetch initiative and employees
    cursor.execute("""
        SELECT i.*, d.Division_Name
        FROM Initiative_Table i
        LEFT JOIN Division_Table d ON i.Division_ID = d.Division_ID
        WHERE i.ID = ?
    """, (id,))
    initiative = cursor.fetchone()

    cursor.execute("""
        SELECT e.Emp_ID, e.Name, e.Role
        FROM Employee_Table e
        INNER JOIN Employee_Initiative_Table ei ON ei.Emp_ID = e.Emp_ID
        WHERE ei.IN_ID = ?
    """, (initiative.IN_ID,))
    employees = cursor.fetchall()

    # Dropdown data
    cursor.execute("SELECT DISTINCT Division_Name FROM Division_Table WHERE Division_Name IS NOT NULL AND Division_Name != ''")
    divisions = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Category FROM Initiative_Table WHERE Category IS NOT NULL AND Category != ''")
    categories = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Emp_ID, Name FROM Employee_Table")
    employee_records = [tuple(row) for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Role FROM Employee_Table WHERE Role IS NOT NULL AND Role != ''")
    roles = [row[0] for row in cursor.fetchall()]


    statuses = ["Pending Approval", "Updated", "Rejected"]

    return render_template('update_initiative.html',
                           initiative=initiative,
                           employees=employees,
                           divisions=divisions,
                           categories=categories,
                           statuses=statuses,
                           employee_records=employee_records,
                           roles=roles,)


