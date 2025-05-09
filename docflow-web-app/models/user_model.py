
import re
from db.db_connection import get_connection

def normalize_name(name):

    """
    Normalize a name for flexible and consistent matching:
    - Converts to lowercase
    - Strips leading/trailing whitespace
    - Collapses multiple spaces
    - Sorts words alphabetically to allow for order-insensitive comparison
      (e.g., "John Doe" = "Doe John")
    """

    name = re.sub(r'\s+', ' ', name.strip().lower())  
    parts = name.split()
    return ' '.join(sorted(parts))  

def get_user_by_email_or_name(user_input):

    """
    Attempts to retrieve a user from the database using either:
    - Exact email match (case-insensitive), or
    - Name match with flexible normalization (case-insensitive and word-order tolerant)
    
    Returns user details as a dictionary if matched, else None.
    """

    conn = get_connection()
    cursor = conn.cursor()

    user_input_normalized = normalize_name(user_input)

    # Fetch all users from the database

    cursor.execute("""
        SELECT ID, Name, Email, password_hash, Role
        FROM User_Table
    """)
    users = cursor.fetchall()
    conn.close()

    for user in users:
        db_id, db_name, db_email, db_password_hash, db_role = user

        # Normalize the database name for comparison
        if (
            user_input.lower() == db_email.strip().lower() or
            normalize_name(db_name) == user_input_normalized
        ):
            return {
                "id": db_id,
                "name": db_name,
                "email": db_email,
                "hashpassword": db_password_hash,
                "role": db_role
            }

    return None
