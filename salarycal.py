#!C:/Python/python.exe
import smtplib
import pymysql
import cgi, cgitb
from datetime import date
from email.mime.text import MIMEText

# Enable CGI traceback for debugging
cgitb.enable()

print("content-type:text/html \r\n\r\n")

today = date.today()
year = today.year

form = cgi.FieldStorage()
pid = form.getvalue("id")

try:
    # Database connection
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="final_laptopproject"
    )
    cur = conn.cursor()

    # Process form submission
    psubmit = form.getvalue("submit")
    if psubmit is not None:
        pempid = form.getvalue("emp")
        pname = form.getvalue("name")
        pemail = form.getvalue("email")
        pmonth = form.getvalue("mon")
        pyear = form.getvalue("year")
        psalary = form.getvalue("salary")
        pwdays = form.getvalue("wdays")
        ppdays = form.getvalue("pdays")
        pleave = form.getvalue("pleave_taken")
        pgross_salary = form.getvalue("grosssalary")

        # Validate required fields
        if not all([pempid, pname, pemail, pmonth, pyear, psalary, pwdays, ppdays, pleave, pgross_salary]):
            raise ValueError("All fields are required")

        try:
            q3 = """INSERT INTO `salary_table`(emp_id, emp_name, Email_Id, month, year, 
                    salary, wdays, pdays, leave_taken, gross_salary) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(q3, (pempid, pname, pemail, pmonth, pyear, psalary,
                             pwdays, ppdays, pleave, pgross_salary))
            conn.commit()

            # Send email with salary details
            try:
                fromaddr = "s.nilesh4321@gmail.com"
                password = "nudohwfqpcevrojw"
                toaddr = pemail
                subject = f"Salary Credited for {pmonth} {pyear}"

                body = f"""Dear {pname},

Your salary for {pmonth} {pyear} has been processed successfully. Below are the details:

Employee ID: {pempid}
Employee Name: {pname}
Month: {pmonth} {pyear}
---------------------------------
Basic Salary: ₹{psalary}
Working Days: {pwdays}
Present Days: {ppdays}
Leave Taken: {pleave}
---------------------------------
Gross Salary: ₹{pgross_salary}

Thank you for your hard work!

Best regards,
ASUS HR Department"""

                msg = MIMEText(body, 'plain', 'utf-8')
                msg['Subject'] = subject
                msg['From'] = fromaddr
                msg['To'] = toaddr

                server = smtplib.SMTP("smtp.gmail.com:587")
                server.ehlo()
                server.starttls()
                server.login(fromaddr, password)
                server.sendmail(fromaddr, [toaddr], msg.as_string())
                server.quit()

                print(f"""
                    <script>
                        alert("Salary data saved and email sent successfully");
                        window.location.href = "./salary.py?id={pid}";
                    </script>
                """)
            except smtplib.SMTPException as e:
                print(f"""
                    <script>
                        alert("Salary data saved but email could not be sent: {str(e)}");
                        window.location.href = "./salary.py?id={pid}";
                    </script>
                """)
            except Exception as e:
                print(f"""
                    <script>
                        alert("Salary data saved but email could not be sent: {str(e)}");
                        window.location.href = "./salary.py?id={pid}";
                    </script>
                """)
        except pymysql.Error as e:
            conn.rollback()
            print(f"""
                <script>
                    alert("Database Error: {str(e)}");
                </script>
            """)

    # Fetch employee data
    q = """SELECT * FROM `adm_emp_addform` WHERE id=%s"""
    cur.execute(q, (pid,))
    res = cur.fetchone()

    if not res:
        raise ValueError("Employee not found")

    salary = res[14]
    Emp = res[10]
    email = res[2]
    name = res[1]

    # Fetch leave data
    q2 = """SELECT * FROM employee_leave_form WHERE EMPId=%s"""
    cur.execute(q2, (Emp,))
    leave_data = cur.fetchone()

    # HTML output
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Employee Salary Management</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-color: #000000; /* ASUS Black */
                --secondary-color: #f8f9fc;
                --accent-color: #FF0000; /* ASUS Red */
                --text-color: #333333;
                --sidebar-width: 250px;
                --transition-speed: 0.3s;
            }}

            body {{
                font-family: 'Nunito', sans-serif;
                background-color: #f8f9fc;
                color: var(--text-color);
                margin: 0;
                padding: 0;
                display: flex;
                min-height: 100vh;
            }}

            .sidebar {{
                width: var(--sidebar-width);
                background: linear-gradient(180deg, var(--primary-color) 0%, #333333 100%);
                color: white;
                height: 100vh;
                position: fixed;
                box-shadow: 0 0.15rem 1.75rem 0 rgba(0, 0, 0, 0.2);
                transition: all var(--transition-speed) ease;
                z-index: 1000;
            }}

            .sidebar-header {{
                padding: 1.5rem 1.5rem 0.5rem;
                font-weight: 800;
                font-size: 1.2rem;
                text-align: center;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 1rem;
            }}

            .sidebar-header h3 {{
                color: #FF0000;
                margin: 0;
                font-size: 1.5rem;
            }}

            .sidebar-header span {{
                color: black;
                font-weight: 400;
            }}

            .nav-menu {{
                padding: 0 1rem;
                margin-top: 1rem;
                overflow-y: auto;
                height: calc(100vh - 100px);
            }}

            .nav-item {{
                margin-bottom: 0.5rem;
                position: relative;
            }}

            .nav-link {{
                color: rgba black;
                padding: 0.75rem 1rem;
                display: flex;
                align-items: center;
                border-radius: 0.35rem;
                text-decoration: none;
                transition: all var(--transition-speed);
            }}

            .nav-link i {{
                margin-right: 0.5rem;
                font-size: 0.85rem;
                width: 20px;
                text-align: center;
            }}

            .nav-link:hover, .nav-link.active {{
                color: white;
                background-color: var(--accent-color);
                transform: translateX(5px);
            }}

            .dropdown-toggle::after {{
                display: inline-block;
                margin-left: auto;
                vertical-align: middle;
                content: "";
                border-top: 0.3em solid;
                border-right: 0.3em solid transparent;
                border-bottom: 0;
                border-left: 0.3em solid transparent;
                transition: transform var(--transition-speed);
            }}

            .dropdown-toggle.collapsed::after {{
                transform: rotate(-90deg);
            }}

            .dropdown-menu {{
                padding-left: 1.5rem;
                max-height: 0;
                overflow: hidden;
                transition: max-height var(--transition-speed) ease-out;
            }}

            .dropdown-menu.show {{
                max-height: 500px;
                transition: max-height var(--transition-speed) ease-in;
            }}

            .main-content {{
                margin-left: var(--sidebar-width);
                width: calc(100% - var(--sidebar-width));
                padding: 2rem;
                transition: all var(--transition-speed);
            }}

            .salary-form {{
                background: white;
                border-radius: 0.35rem;
                box-shadow: 0 0.15rem 1.75rem 0 rgba(0, 0, 0, 0.1);
                padding: 2rem;
                max-width: 800px;
                margin: 0 auto;
                animation: fadeIn 0.5s ease-in-out;
            }}

            .heading {{
                color: var(--accent-color);
                margin-bottom: 1.5rem;
                font-weight: 700;
                position: relative;
                padding-bottom: 0.5rem;
            }}

            .heading::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 50px;
                height: 3px;
                background-color: var(--accent-color);
            }}

            .form-label {{
                font-weight: 600;
                color: var(--text-color);
            }}

            .form-control {{
                border-radius: 0.35rem;
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
                border: 1px solid #ddd;
                transition: all var(--transition-speed);
            }}

            .form-control:focus {{
                border-color: var(--accent-color);
                box-shadow: 0 0 0 0.25rem rgba(255, 0, 0, 0.25);
            }}

            .btn-primary {{
                background-color: var(--accent-color);
                border: none;
                padding: 0.75rem;
                font-weight: 600;
                transition: all var(--transition-speed);
                background-color: var(--accent-color);
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .btn-primary:hover {{
                background-color: #cc0000;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}

            .btn-primary:active {{
                transform: translateY(0);
            }}

            @media (max-width: 768px) {{
                .sidebar {{
                    width: 100%;
                    height: auto;
                    position: relative;
                }}

                .main-content {{
                    margin-left: 0;
                    width: 100%;
                }}
            }}

            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .pulse {{
                animation: pulse 2s infinite;
            }}

            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4); }}
                70% {{ box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }}
            }}

            /* ASUS Branding */
            .asus-badge {{
                position: fixed;
                bottom: 20px;
                left: 20px;
                background-color: var(--primary-color);
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1001;
            }}
        </style>
        <script type="text/javascript">
            function calcDays(){{
                var monthSelect = document.salaryForm.mon.selectedIndex;
                var wdaysField = document.salaryForm.wdays;

                if(monthSelect == 1) wdaysField.value = "31";
                if(monthSelect == 2) wdaysField.value = "28";
                if(monthSelect == 3) wdaysField.value = "31";
                if(monthSelect == 4) wdaysField.value = "30";
                if(monthSelect == 5) wdaysField.value = "31";
                if(monthSelect == 6) wdaysField.value = "30";
                if(monthSelect == 7) wdaysField.value = "31";
                if(monthSelect == 8) wdaysField.value = "31";
                if(monthSelect == 9) wdaysField.value = "30";
                if(monthSelect == 10) wdaysField.value = "31";
                if(monthSelect == 11) wdaysField.value = "30";
                if(monthSelect == 12) wdaysField.value = "31";

                calculatePresentDays();
                calculateGrossSalary();
            }}

            function calculatePresentDays(){{
                var wdays = parseInt(document.salaryForm.wdays.value) || 0;
                var ldays = parseInt(document.salaryForm.pleave_taken.value) || 0;
                document.salaryForm.pdays.value = wdays - ldays;    
            }}

            function calculateGrossSalary(){{
                var sal = parseInt(document.salaryForm.salary.value) || 0;
                var present = parseInt(document.salaryForm.pdays.value) || 0;
                var work = parseInt(document.salaryForm.wdays.value) || 1;
                document.salaryForm.grosssalary.value = Math.round((sal * present)/work);    
            }}

            // Dropdown functionality
            document.addEventListener('DOMContentLoaded', function() {{
                // Toggle dropdown menus
                const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

                dropdownToggles.forEach(toggle => {{
                    toggle.addEventListener('click', function(e) {{
                        e.preventDefault();
                        const menu = this.nextElementSibling;

                        // Close all other dropdowns
                        document.querySelectorAll('.dropdown-menu').forEach(m => {{
                            if (m !== menu) {{
                                m.classList.remove('show');
                                const toggle = m.previousElementSibling;
                                if (toggle) toggle.classList.add('collapsed');
                            }}
                        }});

                        // Toggle current dropdown
                        menu.classList.toggle('show');
                        this.classList.toggle('collapsed');
                    }});
                }});

                // Close dropdowns when clicking outside
                document.addEventListener('click', function(e) {{
                    if (!e.target.closest('.nav-item')) {{
                        document.querySelectorAll('.dropdown-menu').forEach(menu => {{
                            menu.classList.remove('show');
                            const toggle = menu.previousElementSibling;
                            if (toggle) toggle.classList.add('collapsed');
                        }});
                    }}
                }});
            }});
        </script>
    </head>
    <body>
        <!-- Vertical Sidebar Navbar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h3>ASUS <span>Admin</span></h3>
            </div>

            <div class="nav-menu">
                <div class="nav-item">
                    <a href="adm-dashboard2.py" class="nav-link">
                        <i class="fas fa-tachometer-alt"></i>
                        <span>Dashboard</span>
                    </a>
                </div>

                <div class="nav-item">
                    <a href="#" class="nav-link dropdown-toggle">
                        <i class="fas fa-users"></i>
                        <span>Employees</span>
                    </a>
                    <div class="dropdown-menu">
                        <div class="nav-item">
                            <a href="adm-emp-addform.py" class="nav-link">
                                <i class="fas fa-user-plus"></i>
                                <span>Add Employee</span>
                            </a>
                        </div>
                        <div class="nav-item">
                            <a href="adm-emp-list.py" class="nav-link">
                                <i class="fas fa-list"></i>
                                <span>Employee List</span>
                            </a>
                        </div>
                    </div>
                </div>

                <div class="nav-item">
                    <a href="adm-emp-lev.py" class="nav-link">
                        <i class="fas fa-calendar-minus"></i>
                        <span>Leave Requests</span>
                    </a>
                </div>

                <div class="nav-item">
                    <a href="salary.py?id={pid}" class="nav-link active">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Salary</span>
                    </a>
                </div>

                <div class="nav-item">
                    <a href="adm-emp-inventory.py" class="nav-link">
                        <i class="fas fa-laptop"></i>
                        <span>Inventory</span>
                    </a>
                </div>

                <div class="nav-item">
                    <a href="adm-order.py" class="nav-link">
                        <i class="fas fa-shopping-cart"></i>
                        <span>Orders</span>
                    </a>
                </div>

                <div class="nav-item logout">
                    <a href="login1.py" class="nav-link">
                        <i class="fas fa-sign-out-alt"></i>
                        <span>Logout</span>
                    </a>
                </div>
            </div>

            <div class="asus-badge pulse">
                ASUS Admin Portal
            </div>
        </div>

        <div class="main-content">
            <div class="salary-form">
                <center><h4 class="heading">Salary Details for {name}</h4></center>
                <form name="salaryForm" method="post">
                    <div class="mb-3">
                        <label class="form-label">Employee ID</label>
                        <input class="form-control" type="text" name="emp" value="{Emp}" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Employee name</label>
                        <input class="form-control" type="text" name="name" value="{name}" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email ID</label>
                        <input class="form-control" type="text" name="email" value="{email}" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Month</label>
                        <select class="form-control" name="mon" onchange="calcDays()" required>
                            <option value="">Select month</option>
                            <option value="Jan">January</option>
                            <option value="Feb">February</option>
                            <option value="Mar">March</option>
                            <option value="Apr">April</option>
                            <option value="May">May</option>
                            <option value="Jun">June</option>
                            <option value="Jul">July</option>
                            <option value="Aug">August</option>
                            <option value="Sep">September</option>
                            <option value="Oct">October</option>
                            <option value="Nov">November</option>
                            <option value="Dec">December</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Year</label>
                        <input class="form-control" type="text" name="year" value="{year}" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Salary</label>
                        <input class="form-control" type="text" value="{salary}" name="salary" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Working Days</label>
                        <input class="form-control" type="text" name="wdays" placeholder="Working days" required>
                    </div>
    """)

    if leave_data:
        print(f"""
                    <div class="mb-3">
                        <label class="form-label">Leave Taken</label>
                        <input class="form-control" type="text" readonly name="pleave_taken" value="{leave_data[6]}" required>
                    </div>
        """)
    else:
        print("""
                    <div class="mb-3">
                        <label class="form-label">Leave Taken</label>
                        <input class="form-control" type="text" readonly name="pleave_taken" value="0" required>
                    </div>
        """)

    print("""
                    <div class="mb-3">
                        <label class="form-label">Present Days</label>
                        <input class="form-control" type="text" name="pdays" placeholder="Present days" readonly required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Gross Salary</label>
                        <input class="form-control" type="text" name="grosssalary" placeholder="Gross Salary" readonly required>
                    </div>
                    <div class="mb-3">
                        <input class="btn btn-primary form-control pulse" type="submit" name="submit" value="Submit">
                    </div>
                </form>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

except Exception as e:
    print(f"""
        <div class="alert alert-danger">
            <strong>Error:</strong> {str(e)}
        </div>
    """)
finally:
    if 'conn' in locals() and conn.open:
        conn.close()