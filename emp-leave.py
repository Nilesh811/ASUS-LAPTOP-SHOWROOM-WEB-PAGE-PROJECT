#!C:/Python/python.exe
import cgi
import cgitb
import pymysql
import sys
import io
from datetime import datetime

# Enable debugging
cgitb.enable()

# Database connection
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",  # Add your database password if required
        database="final_laptopproject"
    )
    cur = conn.cursor()
except Exception as e:
    print("Content-type: text/html\n")
    print(f"<h1>Database Connection Error: {str(e)}</h1>")
    sys.exit(1)

# Get form data
form = cgi.FieldStorage()
pid = form.getvalue("id")

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Process form submission if submitted
if form.getvalue("submit"):
    pEmpId = form.getvalue("uEmpId")  # Changed from employeeId to uemployeeid
    pemployeeName = form.getvalue("uemployeename")  # Changed from employeeName to uemployeename
    pdepartment = form.getvalue("department")
    pposition = form.getvalue("position")
    pleaveType = form.getvalue("leaveType")
    pdaysRequested = form.getvalue("daysRequested")
    pfromDate = form.getvalue("fromDate")
    ptoDate = form.getvalue("toDate")
    preason = form.getvalue("reason")

    try:
        q2 = """INSERT INTO `employee_leave_form` 
                (EmpId, Employee_name, department, position, leave_type, 
                 days_requested, from_date, to_date, reason, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')"""

        cur.execute(q2, (pEmpId, pemployeeName, pdepartment, pposition,
                         pleaveType, pdaysRequested, pfromDate, ptoDate, preason))
        conn.commit()

        # Success response
        print("Content-type: text/html\n")
        print(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Leave Request Submitted</title>
            <script>
                alert("Leave request submitted successfully!");
                window.location.href = "emp-leave.py?id={pid}";
            </script>
        </head>
        <body>
            <p>If you are not redirected, <a href="emp-leave.py?id={pid}">click here</a>.</p>
        </body>
        </html>
        """)
        sys.exit(0)

    except Exception as e:
        print("Content-type: text/html\n")
        print(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <script>
                alert("Error submitting leave request: {str(e)}");
                window.history.back();
            </script>
        </head>
        <body>
            <p>If you are not redirected, <a href="javascript:history.back()">click here</a>.</p>
        </body>
        </html>
        """)
        sys.exit(1)

# If not submitting, show the form
print("Content-type:text/html\r\n\r\n")



# If not submitting, show the form
print("Content-type:text/html\r\n\r\n")
print(f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom - Leave Request</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {{
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-gray: #333333;
            --asus-light: #f5f5f5;
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;
            --sidebar-width: 250px;
            --transition-speed: 0.3s;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }}

        body {{
            display: flex;
            min-height: 100vh;
            background-color: #f9f9f9;
            overflow-x: hidden;
        }}

        /* Sidebar */
        .sidebar {{
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }}

        .sidebar-header {{
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 0, 0, 0.1);
        }}

        .sidebar-header img {{
            width: 40px;
            margin-right: 10px;
        }}

        .sidebar-header h3 {{
            font-size: 1.2rem;
            color: white;
            font-weight: 700;
        }}

        .sidebar-header span {{
            color: var(--asus-red);
            font-weight: 700;
        }}

        .nav-menu {{
            padding: 20px 0;
        }}

        .nav-item {{
            margin: 5px 0;
        }}

        .nav-link {{
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
            position: relative;
            overflow: hidden;
            font-weight: 500;
        }}

        .nav-link i {{
            margin-right: 15px;
            font-size: 1.1rem;
            color: var(--asus-red);
            transition: all var(--transition-speed) ease;
        }}

        .nav-link:hover {{
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
            transform: translateX(5px);
        }}

        .dropdown-menu {{
            padding-left: 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--transition-speed) ease;
            background: rgba(0, 0, 0, 0.2);
        }}

        .dropdown-menu.show {{
            max-height: 300px;
        }}

        .dropdown-menu a {{
            display: block;
            padding: 10px 15px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
        }}

        .dropdown-menu a:hover {{
            background: rgba(255, 0, 0, 0.2);
            padding-left: 20px;
        }}

        .logout {{
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }}

        /* Main Content */
        .main-content {{
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 30px;
            transition: all var(--transition-speed) ease;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            animation: fadeInDown 0.5s ease;
        }}

        .header h1 {{
            color: var(--asus-gray);
            font-size: 1.8rem;
            position: relative;
        }}

        .header h1::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--asus-red);
        }}

        .user-profile {{
            display: flex;
            align-items: center;
        }}

        .user-profile img {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            object-fit: cover;
            border: 2px solid var(--asus-red);
        }}

        .user-profile span {{
            font-weight: 600;
            color: var(--asus-gray);
        }}

        /* Leave Form */
        .leave-form-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            animation: slideUp 0.5s ease;
        }}

        .form-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }}

        .form-header h2 {{
            color: var(--asus-gray);
            font-size: 1.5rem;
        }}

        .form-header span {{
            color: var(--asus-red);
        }}

        .form-row {{
            display: flex;
            flex-wrap: wrap;
            margin: 0 -15px;
        }}

        .form-group {{
            flex: 1;
            min-width: 250px;
            padding: 0 15px;
            margin-bottom: 20px;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--asus-gray);
        }}

        .form-control {{
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            transition: all var(--transition-speed) ease;
        }}

        .form-control:focus {{
            border-color: var(--asus-red);
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
            outline: none;
        }}

        .select-wrapper {{
            position: relative;
        }}

        .select-wrapper::after {{
            content: '\\f078';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            top: 50%;
            right: 15px;
            transform: translateY(-50%);
            color: var(--asus-gray);
            pointer-events: none;
        }}

        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: all var(--transition-speed) ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}

        .btn-primary {{
            background: var(--asus-red);
            color: white;
        }}

        .btn-primary:hover {{
            background: #e60000;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
        }}

        .btn i {{
            margin-right: 8px;
        }}

        .form-footer {{
            display: flex;
            justify-content: flex-end;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}

        /* Animations */
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-20px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes pulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4);
            }}

            70% {{
                box-shadow: 0 0 0 10px rgba(255, 0, 0, 0);
            }}

            100% {{
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
            }}
        }}

        .pulse {{
            animation: pulse 1.5s infinite;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .sidebar {{
                transform: translateX(-100%);
            }}

            .sidebar.active {{
                transform: translateX(0);
            }}

            .main-content {{
                margin-left: 0;
            }}

            .form-group {{
                min-width: 100%;
            }}
        }}
    </style>
</head>

<body>

    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            <h3>ASUS <span>Showroom</span></h3>
        </div>
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="./emp1-dash.py?id={pid}" class="nav-link active">
                    <i class="fas fa-tachometer-alt"></i>
                    <span> Employee Dashboard</span>
                </a>
            </li>
          
            <li class="nav-item">
                <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                    <i class="fas fa-laptop"></i>Inventory ▼
                </div>
                <ul class="dropdown-menu">
                    <li><a href="./emp-inventory.py?id={pid}">Add Laptop</a></li>
                    <li><a href="./emp-inv-tableview.py?id={pid}">Inventory List</a></li>
                </ul>
            </li>
            <li class="nav-item">
                <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                    <i class="fas fa-calendar-minus"></i>
                    <span>Leave Request ▼</span>
                </div>
                <ul class="dropdown-menu">
                    <li><a href="./emp-leave.py?id={pid}">Request Form</a></li>
                    <li><a href="./emp-leavehis.py?id={pid}">History</a></li>
                </ul>
            </li>
             </li>
          <li class="nav-item">
            <a href="emp-salary-view.py?id={pid}" class="nav-link">
                <i class="fas fa-money-bill-wave"></i>
                <span>salary view</span>
            </a>
        </li>
            <li class="nav-item logout">
                <a href="employee_login.py?id={pid}" class="nav-link">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </li>
        </ul>
    </div>


    <!-- Main Content -->
    <div class="main-content">
        <div class="header">
            <h1>Leave <span>Request</span></h1>
        </div>

        <div class="leave-form-container">
            <div class="form-header">
                <h2>Submit <span>Leave Request</span></h2>
            </div>

            <form id="leaveForm" method="POST" action="emp-leave.py?id={pid}">
                <div class="form-row">
                    <div class="form-group">
                        <label for="employeeId">Employee ID</label>
                        """)
# Fix the SQL query - removed the extra quote and used parameterized query
try:
    q = "SELECT * FROM `adm_emp_addform` WHERE id=%s"
    cur.execute(q, (pid,))
    res = cur.fetchall()

    if res:
        Empid = res[0][10]
        Name = res[0][1]
    else:
        Empid = ""
        Name = ""
except Exception as e:
    Empid = ""
    Name = ""
    print(f"<!-- Error fetching employee data: {str(e)} -->")
print("""
    <input type="text" class="form-control" id="EmpId" name="uEmpId" value="%s"  required>
""" % (Empid))

print("""
                                </div>
</div>
                        <div class="mb-3">
                            <label for="employeeName" class="form-label">Employee Name</label>
                     """)
print("""
                            <input type="text" class="form-control" id="employeeName" name="uemployeename" value="%s" required>
                    """ % (Name))
print("""

                <div class="form-row">
                    <div class="form-group">
                        <label for="department">Department</label>
                        <div class="select-wrapper">
                            <select id="department" name="department" class="form-control" required>
                               <option value="">Select Department</option>
                                <option value="sales">Sales</option>
                                <option value="technical">Technical Support</option>
                                <option value="inventory">Inventory Management</option>
                                <option value="marketing">Marketing</option>
                                <option value="hr">Human Resources</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                            <label for="position">Position</label>
                            <select id="position" name="position" class="form-control form-select" required>
                               <option value="">Select Position</option>
                                <option value="manager">Manager</option>
                                <option value=" Salesassistant">Sales Assistant</option>
                                <option value="technician">Technician</option>
                                <option value=" Sales executive">Sales Executive</option>
                                <option value=" Marketing specialist">Marketing</option>
                                <option value="HR">HR</option>
                                <option value="Inventory ">Inventory</option>
                            </select>
                        </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="leaveType">Leave Type</label>
                        <div class="select-wrapper">
                            <select id="leaveType" name="leaveType" class="form-control" required>
                                <option value="">Select Leave Type</option>
                                <option value="Sick Leave">Sick Leave</option>
                                <option value="Vacation">Vacation</option>
                                <option value="Personal">Personal</option>
                                <option value="Maternity/Paternity">Maternity/Paternity</option>
                                <option value="Bereavement">Bereavement</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="daysRequested">Days Requested</label>
                        <input type="text" id="daysRequested" name="daysRequested" class="form-control" readonly>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="fromDate">From Date</label>
                        <input type="date" id="fromDate" name="fromDate" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="toDate">To Date</label>
                        <input type="date" id="toDate" name="toDate" class="form-control" required>
                    </div>
                </div>

                <div class="form-group">
                    <label for="reason">Reason for Leave</label>
                    <textarea id="reason" name="reason" class="form-control" rows="4"
                        placeholder="Please provide details for your leave request" required></textarea>
                </div>

                <div class="form-footer">
                    <button type="submit" name="submit" value="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i> Submit Request
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Toggle dropdown menu
        function toggleDropdown(element) {{
            const dropdownMenu = element.nextElementSibling;
            dropdownMenu.classList.toggle('show');

            // Change icon based on state
            const icon = element.querySelector('span');
            if (dropdownMenu.classList.contains('show')) {{
                icon.innerHTML = 'Leave Request ▼';
            }} else {{
                icon.innerHTML = 'Leave Request ▶';
            }}
        }}

        // Calculate days between dates
        document.getElementById('fromDate').addEventListener('change', calculateDays);
        document.getElementById('toDate').addEventListener('change', calculateDays);

        function calculateDays() {{
            const fromDate = new Date(document.getElementById('fromDate').value);
            const toDate = new Date(document.getElementById('toDate').value);

            if (fromDate && toDate && fromDate <= toDate) {{
                const diffTime = Math.abs(toDate - fromDate);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                document.getElementById('daysRequested').value = diffDays + ' day(s)';
            }} else {{
                document.getElementById('daysRequested').value = '';
            }}
        }}

        // Form validation
        document.getElementById('leaveForm').addEventListener('submit', function(e) {{
            const fromDate = new Date(document.getElementById('fromDate').value);
            const toDate = new Date(document.getElementById('toDate').value);

            if (fromDate > toDate) {{
                e.preventDefault();
                alert("To Date must be after From Date");
                return false;
            }}
            return true;
        }});
    </script>
</body>
</html>
""")

# Close database connection
conn.close()