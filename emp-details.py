#!C:/Python/python.exe
print("Content-type:text/html\r\n\r\n")

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymysql
import cgi, cgitb, os

cgitb.enable()

con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()
form = cgi.FieldStorage()
q = """select * from `adm-emp-addform`"""
cur.execute(q)
rec = cur.fetchall()
pid = form.getvalue("id")
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ASUS Showroom Employee Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <style>
        :root {
            /* ASUS Brand Colors */
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-dark-red: #CC0000;
            --asus-light-red: rgba(255, 0, 0, 0.1);
            --asus-gray: #333333;
            --asus-light-gray: #f5f5f5;
            --asus-white: #ffffff;
            --asus-blue: #0066cc;

            /* Status Colors */
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;

            /* Layout */
            --sidebar-width: 250px;
            --sidebar-collapsed-width: 70px;
            --transition-speed: 0.3s;
            --border-radius: 6px;
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
            background-color: var(--asus-light-gray);
            color: var(--asus-gray);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* ============ SIDEBAR ============ */
        /* Sidebar */
        .sidebar {
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }

        .sidebar-header {
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 0, 0, 0.1);
        }

        .sidebar-header img {
            width: 40px;
            margin-right: 10px;
        }

        .sidebar-header h3 {
            font-size: 1.2rem;
            color: white;
            font-weight: 700;
        }

        .sidebar-header span {
            color: var(--asus-red);
            font-weight: 700;
        }

        .nav-menu {
            padding: 20px 0;
        }

        .nav-item {
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
        }

        .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
            transform: translateX(5px);
        }

        .dropdown-menu {
            padding-left: 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--transition-speed) ease;
            background: rgba(0, 0, 0, 0.2);
        }

        .dropdown-menu.show {
            max-height: 300px;
        }

        .dropdown-menu a {
            display: block;
            padding: 10px 15px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
        }

        .dropdown-menu a:hover {
            background: rgba(255, 0, 0, 0.2);
            padding-left: 20px;
        }

        .logout {
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }



        /* ============ MAIN CONTENT ============ */
        .main-content {
            margin-left: var(--sidebar-width);
            width: calc(100% - var(--sidebar-width));
            padding: 30px;
            transition: all var(--transition-speed) ease;
        }

        /* ============ EMPLOYEE TABLE ============ */
        .employee-table-container {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            padding: 30px;
            position: relative;
        }

        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .table-header h2 {
            color: var(--asus-gray);
            font-size: 1.8rem;
            display: flex;
            align-items: center;
        }

        .table-header h2 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .quick-actions {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .quick-action-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 15px;
            background-color: var(--asus-red);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .quick-action-btn:hover {
            background-color: var(--asus-dark-red);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .quick-action-btn i {
            font-size: 14px;
        }

        .search-filter {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .search-box {
            flex: 1;
            min-width: 250px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 12px 15px 12px 40px;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .search-box input:focus {
            border-color: var(--asus-red);
            box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
            outline: none;
        }

        .search-box i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--asus-gray);
        }

        .filter-dropdown {
            min-width: 200px;
        }

        .filter-dropdown select {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
            font-size: 1rem;
            background-color: white;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .filter-dropdown select:focus {
            border-color: var(--asus-red);
            box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
            outline: none;
        }

        /* Table wrapper for scrolling */
        .table-wrapper {
            overflow-x: auto;
            max-height: calc(100vh - 300px);
            margin-top: 20px;
            border: 1px solid #eee;
            border-radius: var(--border-radius);
        }

        .employee-table {
            width: 100%;
            min-width: 1200px;
            border-collapse: collapse;
            font-size: 0.95rem;
        }

        .employee-table th {
            background-color: var(--asus-black);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
        }

        .employee-table th:first-child {
            border-top-left-radius: var(--border-radius);
        }

        .employee-table th:last-child {
            border-top-right-radius: var(--border-radius);
        }

        .employee-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .employee-table tr:nth-child(even) {
            background-color: rgba(0, 0, 0, 0.02);
        }

        .employee-table tr:last-child td {
            border-bottom: none;
        }

        .employee-table tr:hover {
            background-color: var(--asus-light-red);
        }

        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-align: center;
            min-width: 70px;
        }

        .status-active {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
        }

        .status-inactive {
            background-color: rgba(244, 67, 54, 0.1);
            color: var(--negative);
        }

        /* Action buttons */
        .action-btns {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 6px 12px;
            border: none;
            border-radius: var(--border-radius);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }

        .btn i {
            font-size: 0.9rem;
        }

        .btn-view {
            background-color: rgba(33, 150, 243, 0.1);
            color: var(--info);
        }

        .btn-view:hover {
            background-color: rgba(33, 150, 243, 0.2);
        }

        .btn-edit {
            background-color: rgba(255, 152, 0, 0.1);
            color: var(--warning);
        }

        .btn-edit:hover {
            background-color: rgba(255, 152, 0, 0.2);
        }

        .btn-delete {
            background-color: rgba(244, 67, 54, 0.1);
            color: var(--negative);
        }

        .btn-delete:hover {
            background-color: rgba(244, 67, 54, 0.2);
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--asus-red);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--asus-dark-red);
        }

        /* ============ RESPONSIVE ADJUSTMENTS ============ */
        @media (max-width: 1200px) {
            .employee-table {
                min-width: 1000px;
            }
        }

        @media (max-width: 992px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
            }

            .sidebar-header h3,
            .nav-link span,
            .dropdown-toggle::after {
                display: none;
            }

            .nav-link {
                justify-content: center;
                padding: 12px 5px;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.2rem;
            }

            .main-content {
                margin-left: var(--sidebar-collapsed-width);
                width: calc(100% - var(--sidebar-collapsed-width));
            }
        }

        @media (max-width: 768px) {
            .main-content {
                padding: 20px;
            }

            .employee-table-container {
                padding: 20px;
            }

            .table-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }

            .search-filter {
                flex-direction: column;
            }

            .search-box,
            .filter-dropdown {
                width: 100%;
            }

            .table-wrapper {
                max-height: calc(100vh - 250px);
            }
        }

        @media (max-width: 576px) {
            .sidebar {
                width: 0;
                overflow: hidden;
            }

            .main-content {
                margin-left: 0;
                width: 100%;
            }

            .action-btns {
                flex-direction: column;
                gap: 5px;
            }

            .btn {
                width: 100%;
                justify-content: center;
            }

            .table-wrapper {
                max-height: calc(100vh - 220px);
            }
        }
    </style>
</head>

<body>

    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            <h3>EMPLOYEE <span>DASHBOARD</span></h3>
        </div>
        <ul class="nav-menu">
            <li class="nav-item">
               """)
print("""
                <a href="./emp1-dash.py?id=%s" class="nav-link active">
                       """ % pid)
print("""
                    <i class="fas fa-tachometer-alt"></i>
                    <span> Employee Dashboard</span>
                </a>
            </li>

            <li class="nav-item">
                <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                    <i class="fas fa-laptop"></i>Inventory ▼
                </div>
                <ul class="dropdown-menu">
                    <li><a href="./emp-inventory.py?id=%s">Add Laptop</a></li>
                                              """ % pid)
print("""
                    <li><a href="./emp-inv-tableview.py?id=%s">Inventory List</a></li>
                                              """ % pid)
print("""
                </ul>
            </li>
            <li class="nav-item">
                <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                    <i class="fas fa-calendar-minus"></i>
                    <span>Leave Request ▼</span>
                </div>
                <ul class="dropdown-menu">
                    <li><a href="./emp-leave.py?id=%s">Request Form</a></li>
                           """ % pid)
print("""
                    <li><a href="./emp-leavehis.py?id=%s">History</a></li>
                           """ % pid)
print("""
                </ul>
            </li>
            <li class="nav-item">
                <a href="./emp-salary-view.py?id=%s" class="nav-link">
                    <i class="fas fa-money-bill-wave"></i>
                    <span>Salary View</span>
                </a>
            </li>
            <li class="nav-item logout">
                <a href="employee_login.py?id=%s" class="nav-link">
                       """ % pid)
print("""
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </li>
        </ul>
    </div>


    <!-- Main Content -->
    <div class="main-content">
        <div class="employee-table-container">
            <div class="table-header">
                <h2><i class="fas fa-users"></i> Employee Details</h2>
                <div class="quick-actions">

                </div>
            </div>

            <div class="search-filter">
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="employeeSearch" placeholder="Search employees..." class="form-control">
                </div>

            </div>

            <div class="table-wrapper">
                <table class="employee-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>DOB</th>
                            <th>Gender</th>
                            <th>Address</th>
                            <th>City</th>
                            <th>State</th>
                            <th>Pincode</th>
                            <th>Emp ID</th>
                            <th>Join Date</th>
                            <th>Department</th>
                            <th>Position</th>
                            <th>Salary</th>
                            <th>Shift</th>
                            <th>Username</th>
                            <th>Password</th>
                        </tr>
                    </thead>
                    <tbody>
""")
for i in rec:
    print(f"""
                        <tr>
                            <td>{i[0]}</td>
                            <td>{i[1]}</td>
                            <td>{i[2]}</td>
                            <td>{i[3]}</td>
                            <td>{i[4]}</td>
                            <td>{i[5]}</td>
                            <td>{i[6]}</td>
                            <td>{i[7]}</td>
                            <td>{i[8]}</td>
                            <td>{i[9]}</td>
                            <td>{i[10]}</td>
                            <td>{i[11]}</td>
                            <td>{i[12]}</td>
                            <td>{i[13]}</td>
                            <td>{i[14]}</td>
                            <td>{i[15]}</td>
                            <td>{i[16]}</td>
                            <td>••••••••</td>
                        </tr>
""")
print("""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Function to toggle dropdown menus
        function toggleDropdown(element) {
            const dropdownMenu = element.nextElementSibling;
            dropdownMenu.classList.toggle('show');
            element.classList.toggle('active');
        }

        // Function to filter employees
        function filterEmployees() {
            const searchValue = document.getElementById('employeeSearch').value.toLowerCase();
            const departmentValue = document.getElementById('departmentFilter').value;
            const rows = document.querySelectorAll('.employee-table tbody tr');

            rows.forEach(row => {
                const name = row.cells[1].textContent.toLowerCase();
                const department = row.cells[12].textContent;

                const nameMatch = name.includes(searchValue);
                const departmentMatch = departmentValue === '' || department === departmentValue;

                if (nameMatch && departmentMatch) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        // Add event listeners for instant filtering
        document.getElementById('employeeSearch').addEventListener('input', filterEmployees);
        document.getElementById('departmentFilter').addEventListener('change', filterEmployees);
    </script>
</body>
</html>
""")
con.commit()
con.close()