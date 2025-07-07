#!C:/Python/python.exe
print("Content-type:text/html\r\n\r\n")

import pymysql
import cgi, cgitb

cgitb.enable()

# Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

# Process form submission
form = cgi.FieldStorage()
paccept = form.getvalue("accept")
pdecline = form.getvalue("decline")
pid = form.getvalue("id")

if paccept:
    cur.execute("UPDATE employee_leave_form SET status='approved' WHERE id=%s", (pid,))
    con.commit()
    print("""
    <script>alert("Leave approved successfully"); </script>""")

elif pdecline:
    cur.execute("UPDATE employee_leave_form SET status='rejected' WHERE id=%s", (pid,))
    con.commit()
    print("""
    <script>alert("Leave rejected successfully"); </script>""")

# Fetch pending leave requests
cur.execute("SELECT * FROM employee_leave_form WHERE status='pending'")
rec = cur.fetchall()
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Leave Requests</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-gray: #333333;
            --asus-light: #f5f5f5;
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;
            --sidebar-width: 250px;
            --sidebar-collapsed-width: 70px;
            --transition-speed: 0.3s;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            display: flex;
            min-height: 100vh;
            background-color: #f9f9f9;
            overflow-x: hidden;
        }

        /* Sidebar styles */
        .sidebar {
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }

        .sidebar-header {
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transition: all var(--transition-speed) ease;
            background: rgba(255, 0, 0, 0.1);
        }

        .sidebar-header img {
            width: 40px;
            margin-right: 10px;
            transition: all var(--transition-speed) ease;
        }

        .sidebar-header h3 {
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all var(--transition-speed) ease;
        }

        .sidebar-header span {
            color: var(--asus-red);
            font-weight: 700;
        }

        .nav-menu {
            padding: 20px 0;
        }

        .nav-item {
            position: relative;
            margin: 5px 0;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
            position: relative;
            overflow: hidden;
            font-weight: 500;
        }

        .nav-link i {
            margin-right: 15px;
            font-size: 1.1rem;
            color: var(--asus-red);
            transition: all var(--transition-speed) ease;
            min-width: 20px;
        }

        .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
            transform: translateX(5px);
        }

        .nav-link:hover i {
            transform: scale(1.2);
            color: white;
        }

        .nav-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--asus-red);
            transform: scaleY(0);
            transform-origin: center;
            transition: transform var(--transition-speed) ease;
        }

        .nav-link:hover::before {
            transform: scaleY(1);
        }

        .nav-link.active {
            background: rgba(255, 0, 0, 0.2);
            padding-left: 25px;
        }

        .nav-link.active i {
            color: white;
            transform: scale(1.1);
        }

        .nav-link.active::before {
            transform: scaleY(1);
        }

        .dropdown-menu {
            padding-left: 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--transition-speed) ease;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 0 0 8px 8px;
        }

        .dropdown-menu.show {
            max-height: 300px;
            animation: dropdownOpen 0.4s ease forwards;
        }

        @keyframes dropdownOpen {
            0% {
                opacity: 0;
                transform: translateY(-10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .dropdown-menu .nav-link {
            padding: 10px 20px 10px 45px;
            font-size: 0.9rem;
            background: transparent;
        }

        .dropdown-menu .nav-link:hover {
            background: rgba(255, 0, 0, 0.1);
        }

        .dropdown-toggle {
            cursor: pointer;
        }

        .dropdown-toggle::after {
            content: '\f078';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 20px;
            transition: all var(--transition-speed) ease;
        }

        .dropdown-toggle.active::after {
            transform: rotate(180deg);
            color: white;
        }

        .logout {
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }

        .logout .nav-link {
            color: var(--asus-red);
        }

        .logout .nav-link i {
            color: var(--asus-red);
        }

        .logout .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            color: white;
        }

        .logout .nav-link:hover i {
            color: white;
        }

        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            width: calc(100% - var(--sidebar-width));
            padding: 30px;
            transition: all var(--transition-speed) ease;
        }

        /* Leave Requests Container with Overflow */
        .leave-requests-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            padding: 30px;
            animation: fadeIn 0.6s ease;
            overflow: hidden;
        }

        .table-wrapper {
            overflow-x: auto;
            max-height: 70vh;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            position: relative;
            margin-top: 20px;
        }

        /* Table Styles */
        .requests-table {
            width: 100%;
            border-collapse: collapse;
            min-width: 900px;
        }

        .requests-table th,
        .requests-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .requests-table th {
            background: var(--asus-black);
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        /* Status Styles */
        .status-pending {
            color: var(--warning);
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(255, 152, 0, 0.15);
            display: inline-block;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .status-approved {
            color: var(--positive);
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(76, 175, 80, 0.15);
            display: inline-block;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .status-declined {
            color: var(--negative);
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(244, 67, 54, 0.15);
            display: inline-block;
            font-weight: 600;
            font-size: 0.85rem;
        }

        /* Action Buttons */
        .btn {
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.85rem;
            border: none;
        }

        .btn-success {
            background-color: #28a745;
            color: white;
        }

        .btn-success:hover {
            background-color: #218838;
        }

        .btn-danger {
            background-color: #dc3545;
            color: white;
        }

        .btn-danger:hover {
            background-color: #c82333;
        }

        .btn-sm {
            padding: 5px 10px;
            font-size: 0.75rem;
        }

        .mt-2 {
            margin-top: 0.5rem;
        }

        /* Row hover effect */
        .requests-table tr {
            transition: all 0.3s ease;
        }

        .requests-table tr:hover {
            background: rgba(0, 0, 0, 0.02);
        }

        /* Scrollbar styling */
        .table-wrapper::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        .table-wrapper::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .table-wrapper::-webkit-scrollbar-thumb {
            background: var(--asus-red);
            border-radius: 10px;
        }

        .table-wrapper::-webkit-scrollbar-thumb:hover {
            background: #d90000;
        }

        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-content {
                padding: 20px 15px;
            }

            .leave-requests-container {
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <!-- Vertical Sidebar Navbar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            <h3>ASUS <span>Admin Dashboard</span></h3>
        </div>

        <div class="nav-menu">
            <div class="nav-item">
                <a href="adm-dashboard2.py" class="nav-link">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </div>

            <div class="nav-item">
                <div class="nav-link dropdown-toggle">
                    <i class="fas fa-users"></i>
                    <span>Employees</span>
                </div>
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
                <a href="adm-emp-lev.py" class="nav-link active">
                    <i class="fas fa-calendar-minus"></i>
                    <span>Leave Requests</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="salary.py" class="nav-link">
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
                <a href="index.py" class="nav-link">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <div class="leave-requests-container">
            <h2>Employee Leave Requests</h2>

            <div class="table-wrapper">
                <table class="requests-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Employee ID</th>
                            <th>Employee Name</th>
                            <th>Department</th>
                            <th>Position</th>
                            <th>Leave Type</th>
                            <th>days_requested</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Reason</th>
                            <th>Status</th>
                            
                        </tr>
                    </thead>
                    <tbody>
""")

# Table rows with leave requests
for i in rec:
    print(f"""
                        <form method="post">
                            <tr>
                                <input type="hidden" name="id" value="{i[0]}">
                                <td>{i[0]}</td>
                                <td>{i[1]}</td>
                                <td>{i[2]}</td>
                                <td>{i[3]}</td>
                                <td>{i[4]}</td>
                                <td>{i[5]}</td>
                                <td>{i[6]}</td>
                                <td>{i[7]}</td>
                                <td>{i[8]}</td>
                                <td><span class="status-pending">{i[9]}</span></td>
                                <td>
                                    <input class="btn btn-success btn-sm" type="submit" name="accept" value="Accept">
                                    <input class="btn btn-danger btn-sm mt-2" type="submit" name="decline" value="Decline">
                                </td>
                            </tr>
                        </form>
""")

print("""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Dropdown functionality
        document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
            toggle.addEventListener('click', function () {
                this.classList.toggle('active');
                const menu = this.nextElementSibling;
                menu.classList.toggle('show');

                // Close other dropdowns when opening a new one
                document.querySelectorAll('.dropdown-toggle').forEach(otherToggle => {
                    if (otherToggle !== this) {
                        otherToggle.classList.remove('active');
                        otherToggle.nextElementSibling.classList.remove('show');
                    }
                });
            });
        });

        // Enhanced table row hover effect
        document.querySelectorAll('.requests-table tr').forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.style.transform = 'translateX(5px)';
            });

            row.addEventListener('mouseleave', () => {
                row.style.transform = 'translateX(0)';
            });
        });
    </script>
</body>
</html>
""")

# Close database connection
cur.close()
con.close()