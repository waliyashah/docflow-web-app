# 🗂️ DocFlow – From Static Docs to Live Workflow

A centralized, role-based **Initiative Management and Document Tracking System** developed  to digitize and streamline the oversight of strategic initiatives and compliance reports. The project began with the extraction of descriptive initiative data from static Word documents, followed by a structured ETL (Extract, Transform, Load) process implemented in Python to convert unstructured content into a clean, normalized format suitable for relational storage. The transformed data was integrated into a **Microsoft SQL Server** database with fully normalized tables for initiatives, employees, divisions, users, and reports.

On top of this robust backend, a dynamic and user-friendly **Flask web application** was developed to support real-time interaction. The system enables authenticated users to perform core operations such as **adding, editing, deleting, sorting, filtering, searching**, and **viewing initiatives**, while linking associated employee and division records. A comprehensive **reporting module** was also integrated, allowing users to generate and export initiative data in **PDF format**.

The application features a **role-based authentication and authorization** system where users are categorized as Managers, Approvers, or General Users. Managers can submit and edit initiatives, which are routed through an approval workflow, while Approvers have the ability to approve, reject, or update submissions. All user actions are tracked through an **audit logging system**, and key approval status changes trigger notifications within the interface. This solution eliminates the inefficiencies of static document workflows and ensures a scalable, secure, and auditable digital platform for organizational planning and compliance tracking.

---

## 🚀 Features

- ✅ **Role-Based Access** (User, Manager, Approver)
- 🧾 **Add, Edit, Delete Initiatives**
- 🧑‍🤝‍🧑 **Multi-employee Assignment per Initiative**
- 🗂️ **Division Management**
- 🔒 **Approval Workflow with Audit Logs**
- 📥 **PDF Export of Reports**
- 🔔 **Notifications for Pending Approvals**
- 🧾 **Action Logging with Timestamp and Actor**

---

## 🔧 Technologies Used

- **Backend**: Python (Flask, Flask-Session, WTForms, Werkzeug)
- **Authentication & Security**: Werkzeug password hashing, Flask session management
- **Frontend**: HTML, CSS, Bootstrap (no JS for core logic)
- **Database**: Microsoft SQL Server (via pyodbc)
- **PDF Export**: xhtml2pdf
- **Form Handling**: WTForms (for structured, secure input validation)
- **ETL & Scripting**: Python (pandas, python-docx)
- **IDE**: Visual Studio Code
- **DBMS**: SQL Server Management Studio (SSMS)

---

## 🏗 Project Structure (MVC)

The application follows a modular **Model-View-Controller (MVC)** architecture to ensure clear separation between data logic, routing control, and user interface. This structure promotes maintainability, scalability, and ease of collaboration.

web_app/
├── db/             # DB connection config
├── models/         # Model: SQL logic (user, initiative)
├── routes/         # Controller: All route logic
├── static/         # View: CSS/JS assets
├── templates/      # View: HTML templates
├── app.py          # App initialization
├── config.py       # Loads environment/config values

---


## 🔐 Authentication and Roles

- **User**: Basic view permissions
- **Manager**: Can add/edit initiatives; changes marked as `Pending Approval`
- **Approver**: Can directly approve/reject changes; bypasses pending state

Role enforcement is handled using custom decorators in `decorator.py`.

---


## ⚙️ How the Logic Works

1. **Login & Authorization**
   - Implemented in `routes/auth.py` and `models/user_model.py`.
   - Users log in with credentials validated against the `User_Table`.
   - Session-based authentication is enforced using decorators in `routes/decorators.py`, supporting role-based access (User, Manager, Approver).

2. **Dashboard Interaction**
   - After login, users access a dashboard where initiatives are displayed with dynamic **filtering**, **searching**, and **sorting**.
   - Data is queried from SQL Server via `models/initiative_model.py` and rendered using Flask templates.

3. **Initiative Management**
   - Managed via `routes/initiative.py` and `routes/update_initiative.py`.
   - Users can **add**, **edit**, or **delete** initiatives.
   - Managers’ changes are auto-flagged as `Pending Approval` with `Needs_Approval = 1`.

4. **Approval Workflow**
   - Approvers access a filtered view through `routes/approval.py`.
   - A **notification badge** displays the count of pending approvals.
   - Approvers can approve, reject, or update entries. Approved actions clear the flag and finalize the initiative.

5. **Audit Logging**
   - All modifications are recorded in the `ActionLog` table.
   - Logged via `routes/log.py`, capturing who made what change and when.

6. **PDF Export**
   - Users can export filtered or full initiative data using a DOM-based export rendered with `xhtml2pdf`.
   - Formatting and full text expansion handled client-side before rendering.


---


## 🗃️ Database Schema Overview

- `User_Table`
- `Division_Table`
- `Initiative_Table`
- `Employee_Table`
- `Employee_Initiative` (junction)
- `ActionLog` (audit trail)
- `Reports` (initiative-based documents)

---

## 🗺️ Entity-Relationship Diagram (ERD)

The ERD below illustrates how core entities like initiatives, employees, divisions, reports, and users are related.


![ERD](screenshots/erd.png)

---

## 📦 Dependencies

Key libraries used:

- Flask  
- Flask-Session  
- pyodbc  
- python-dotenv  
- xhtml2pdf  
- jinja2  
- pandas  

All dependencies are listed in `requirements.txt`.
[View full requirements](./requirements.txt)


---

## 🖼️ Application Previews

### 🔐 Login Page
![Login](screenshots/login.png)

### 🏠 Dashboard
![Dashboard](screenshots/dashboard.png)

### 🔍 Filter Initiatives
![Filter](screenshots/filter.png)

### ➕ Add New Initiative
![Add Initiative](screenshots/add_form.png)

### 📄 Initiatives Table 
![Table](screenshots/table.png)

---

## 🧑‍💻 Author

**Waliya Shah**  
📍 Springfield, MA  
📧 waliyashah@yahoo.com
📧 waliyashah00@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/waliyashah)