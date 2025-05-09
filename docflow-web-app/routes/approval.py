# ✅ Add the following routes to your Flask backend (e.g. inside routes/initiative.py or a new file like routes/approval.py)

from flask import Blueprint, request, jsonify, session
from db.db_connection import get_connection
from routes.decorators import role_required

# Register the approval blueprint
approval_bp = Blueprint('approval', __name__)

@approval_bp.route('/approve_initiative/<in_id>', methods=['POST'])
@role_required('Approver')

# Approve an initiative
# This route is for approving an initiative and logging the action

def approve_initiative(in_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Update initiative status
    cursor.execute(
        """
        UPDATE Initiative_Table
        SET Status = 'Approved', Needs_Approval = 0
        WHERE IN_ID = ?
        """, (in_id,)
    )

    # ✅ Record the approval action in ActionLog
    performed_by = session.get('name') or session.get('email')
    performed_role = session.get('role')
    cursor.execute(
        """
        INSERT INTO ActionLog (IN_ID, Action_Type, Performed_By, Performed_Role)
        VALUES (?, ?, ?, ?)
        """, (in_id, 'Approved', performed_by, performed_role)
    )

    conn.commit()
    return jsonify({'success': True})


# Reject an initiative
# This route is for rejecting an initiative and logging the action

@approval_bp.route('/reject_initiative/<in_id>', methods=['POST'])
@role_required('Approver')
def reject_initiative(in_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Update initiative's rejection status
    cursor.execute(
        """
        UPDATE Initiative_Table
        SET Status = 'Rejected', Needs_Approval = 0
        WHERE IN_ID = ?
        """, (in_id,)
    )

     # ✅ Record the rejection action in ActionLog
    performed_by = session.get('name') or session.get('email')
    performed_role = session.get('role')
    cursor.execute(
        """
        INSERT INTO ActionLog (IN_ID, Action_Type, Performed_By, Performed_Role)
        VALUES (?, ?, ?, ?)
        """, (in_id, 'Rejected', performed_by, performed_role)
    )

    conn.commit()
    return jsonify({'success': True})
