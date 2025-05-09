from db.db_connection import get_connection

# Fetch all initiatives with related division details, assigned employees, roles, and participants count.
def get_all_initiatives():
    """
    Fetch all initiatives with related Division and Employee details.
    """
    conn = get_connection()
    if not conn:
        return []   # Return empty list if connection fails

    try:
        # SQL query to join Initiative, Division, and Employee tables
        # Aggregates employee info per initiative using STRING_AGG
        # Groups and orders initiatives by their ID
        query = """
        SELECT 
            i.ID,
            i.IN_ID,
            i.Title,
            i.Category,
            i.Status,
            i.Year,
            i.Description,
            d.Division_ID,
            d.Division_Name,
            STRING_AGG(e.Emp_ID, ', ') AS Employee_IDs,
            STRING_AGG(e.Name, ', ') AS Employee_Names,
            STRING_AGG(e.Role, ', ') AS Employee_Roles,
            COUNT(e.Emp_ID) AS Participants
        FROM Initiative_Table i
        LEFT JOIN Division_Table d ON i.Division_ID = d.Division_ID
        LEFT JOIN Employee_Initiative_Table ei ON i.IN_ID = ei.IN_ID
        LEFT JOIN Employee_Table e ON ei.Emp_ID = e.Emp_ID
        GROUP BY i.ID, i.IN_ID, i.Title, i.Category, i.Status, i.Year, i.Description, d.Division_ID, d.Division_Name
        ORDER BY i.ID;
        """
        cursor = conn.cursor()  # Create a cursor object using the connection
        cursor.execute(query) # Execute the query

        # Extract column names from the query result
        columns = [col[0] for col in cursor.description]

         # Fetch all rows of results
        rows = cursor.fetchall()

         # Convert each row to a dictionary using column names
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print("Error fetching initiatives:", e)
        return []
    finally:
        conn.close()


# Fetch unique values for dropdowns dynamically.
from db.db_connection import get_connection
# Fetch unique values for dropdowns dynamically.
def get_filter_options():
    """ Fetch unique values for dropdowns dynamically. """
    conn = get_connection()
    if not conn:
        return {}

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Category FROM Initiative_Table  WHERE Category IS NOT NULL ORDER BY Category")
        categories = [row[0] for row in cursor.fetchall()]

        # Fetch distinct, Uniques, non-empty Division Names
        cursor.execute("SELECT DISTINCT Division_Name FROM Division_Table  WHERE Division_Name IS NOT NULL AND TRIM(Division_Name) <> '' ORDER BY Division_Name")
        divisions = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT Status FROM Initiative_Table  WHERE Status IS NOT NULL  ORDER BY Status")
        statuses = [row[0] for row in cursor.fetchall()]
        
        # Fetch distinct Year values in descending order
        cursor.execute("SELECT DISTINCT Year FROM Initiative_Table  WHERE Year IS NOT NULL ORDER BY Year DESC")
        years = [row[0] for row in cursor.fetchall()]

        return {
            'categories': categories,
            'divisions': divisions,
            'statuses': statuses,
            'years': years
        }
    finally:
        conn.close()


# Fetch all initiatives with related book details, assigned employees, roles, and participants count.
def search_initiatives(filter_options):
    """Search initiatives based on multiple filters."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()

        # Base SQL Query
        base_query = """
        SELECT 
            i.ID,
            i.IN_ID, 
            i.Title,
            i.Category, 
            i.Status, 
            i.Year,
            i.Description,
            d.Division_Name,
            STRING_AGG(COALESCE(e.Emp_ID, 'N/A'), ', ') AS Employee_IDs,
            STRING_AGG(COALESCE(e.Name, 'Unknown'), ', ') AS Employee_Names,
            STRING_AGG(COALESCE(e.Role, 'Not Assigned'), ', ') AS Employee_Roles,   
            COUNT(e.Emp_ID) AS Participants
        FROM Initiative_Table i
        LEFT JOIN Division_Table d ON i.Division_ID = d.Division_ID
        LEFT JOIN Employee_Initiative_Table ei ON i.IN_ID = ei.IN_ID
        LEFT JOIN Employee_Table e ON ei.Emp_ID = e.Emp_ID
        """

        # Filtering Conditions
        conditions = []
        parameters = []

         # Filter by category if not "all"
        if filter_options["category"] != "all":
            conditions.append("i.Category = ?")
            parameters.append(filter_options["category"])

        # Handle multiple divisions
        divisions = filter_options.get("division", ["all"])
        if len(divisions) == 1 and divisions[0] == "all":
            pass  # No condition added
        else:
            placeholders = ", ".join(["?" for _ in divisions])
            conditions.append(f"d.Division_Name IN ({placeholders})")
            parameters.extend(divisions)

        if filter_options["status"] != "all":
            conditions.append("i.Status = ?")
            parameters.append(filter_options["status"])

        if filter_options["year"] != "all" and filter_options["year"].isdigit():
            conditions.append("i.Year = ?")
            parameters.append(filter_options["year"])

         # General keyword search: matches Initiative ID, Employee ID, or Employee Name
        if filter_options["search_query"]:
            conditions.append("(i.IN_ID LIKE ? OR e.Emp_ID LIKE ? OR e.Name LIKE ?)")
            parameters.extend(['%' + filter_options["search_query"] + '%'] * 3)

        # Apply filtering conditions before GROUP BY
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += """
        GROUP BY i.ID, i.IN_ID, i.Title, i.Category, i.Status, i.Year, i.Description, d.Division_Name
        ORDER BY i.ID;
        """

        # Convert result into list of dictionaries
        cursor.execute(base_query, parameters)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print("Error in search_initiatives:", e)
        return []
    finally:
        # Always close the database connection
        conn.close()

# Fetch all reports for a given initiative by IN_ID

from db.db_connection import get_connection
def get_reports_by_initiative(in_id):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Report_ID, Title, Category, Regulatory_Report, Due_Date, Type, Report_Link
            FROM Report_Table
            WHERE IN_ID = ?
        """, (in_id,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching reports for IN_ID {in_id}: {e}")
        return []
    finally:
        conn.close()


# Fetch the number of reports for a given initiative by IN_ID
def get_report_count_by_initiative(in_id):
    conn = get_connection()
    if not conn:
        return 0
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Report_Table WHERE IN_ID = ?", (in_id,))
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error counting reports for IN_ID {in_id}: {e}")
        return 0
    finally:
        conn.close()


# Fetch all reports from the Report_Table
def get_all_reports():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Report_ID, Title, Category, Regulatory_Report, Due_Date, Type, Report_Link, IN_ID
            FROM Report_Table
            ORDER BY Due_Date
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching all reports: {e}")
        return []
    finally:
        conn.close()
