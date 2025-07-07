#!C:/Python/python.exe
print("Content-type:text/html\r\n\r\n")

import pymysql
import cgi, cgitb, os

cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

q = """select * from `adm_emp_addform`"""
cur.execute(q)
rec = cur.fetchall()

print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Employee List</title>
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

        /* Vertical Navbar with Enhanced ASUS Theme */
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

        /* Employee List Container */
        .employee-table-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            position: relative;
            height: calc(100vh - 100px);
            display: flex;
            flex-direction: column;
        }

        /* Fixed header section */
        .table-header-container {
            position: sticky;
            top: 0;
            background: white;
            z-index: 100;
            padding: 20px 30px 0 30px;
            margin: -30px -30px 0 -30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .table-header h2 {
            color: var(--asus-gray);
            font-size: 1.8rem;
        }

        .table-header h2 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .quick-actions {
            display: flex;
            gap: 15px;
        }

        .quick-action-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 15px;
            background-color: var(--asus-red);
            color: white;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .quick-action-btn:hover {
            background-color: #cc0000;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .quick-action-btn i {
            font-size: 14px;
        }

        .search-filter {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }

        .search-box {
            flex: 1;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 12px 15px 12px 40px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
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
            border-radius: 5px;
            font-size: 1rem;
            background-color: white;
        }

        /* Scrollable table section */
        .scrollable-table-container {
            flex: 1;
            overflow-y: auto;
            padding: 0 30px;
            margin-top: 10px;
        }

        .employee-table {
            width: 100%;
            border-collapse: collapse;
            position: relative;
        }

        /* Fixed column headers */
        .employee-table thead th {
            position: sticky;
            top: 0;
            background-color: var(--asus-black);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            z-index: 10;
        }

        .employee-table th:first-child {
            border-top-left-radius: 8px;
        }

        .employee-table th:last-child {
            border-top-right-radius: 8px;
        }

        .employee-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .employee-table tr:last-child td {
            border-bottom: none;
        }

        .employee-table tr:hover {
            background-color: rgba(255, 0, 0, 0.03);
        }

        .status-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .status-active {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
        }

        .status-inactive {
            background-color: rgba(244, 67, 54, 0.1);
            color: var(--negative);
        }

        .action-btns {
            display: flex;
            gap: 10px;
        }

        .btn {
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 5px;
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

        .pagination {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            border-top: 1px solid #eee;
            position: sticky;
            bottom: 0;
            background: white;
            z-index: 5;
        }

        .pagination-info {
            color: var(--asus-gray);
            font-size: 0.9rem;
        }

        .pagination-controls {
            display: flex;
            gap: 10px;
        }

        .page-btn {
            padding: 8px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .page-btn:hover {
            background: #f0f0f0;
        }

        .page-btn.active {
            background: var(--asus-red);
            color: white;
            border-color: var(--asus-red);
        }

        /* Column specific adjustments */
        .employee-table td:nth-child(1), /* # */
        .employee-table td:nth-child(4), /* Phone */
        .employee-table td:nth-child(10), /* Pincode */
        .employee-table td:nth-child(11), /* Empid */
        .employee-table td:nth-child(15) { /* Salary */
            text-align: center;
            width: 60px;
        }

        .employee-table td:nth-child(2), /* Name */
        .employee-table td:nth-child(3), /* Email */
        .employee-table td:nth-child(16), /* Shift */
        .employee-table td:nth-child(17), /* Username */
        .employee-table td:nth-child(18), /* Password */
        .employee-table td:nth-child(19) { /* Confirm Password */
            max-width: 120px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .employee-table td:nth-child(6), /* Gender */
        .employee-table td:nth-child(7), /* Address */
        .employee-table td:nth-child(8), /* City */
        .employee-table td:nth-child(9), /* State */
        .employee-table td:nth-child(12), /* Join Date */
        .employee-table td:nth-child(13), /* Department */
        .employee-table td:nth-child(14) { /* Position */
            max-width: 100px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Responsive adjustments */
        @media (max-width: 1200px) {
            .employee-table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
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

            .pagination {
                flex-direction: column;
                gap: 15px;
            }
        }

        /* Scrollbar styling */
        .scrollable-table-container::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        .scrollable-table-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .scrollable-table-container::-webkit-scrollbar-thumb {
            background: var(--asus-red);
            border-radius: 10px;
        }

        .scrollable-table-container::-webkit-scrollbar-thumb:hover {
            background: #cc0000;
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
                <div class="nav-link dropdown-toggle active">
                    <i class="fas fa-users"></i>
                    <span>Employees</span>
                </div>
                <div class="dropdown-menu show">
                    <div class="nav-item">
                        <a href="adm-emp-addform.py" class="nav-link">
                            <i class="fas fa-user-plus"></i>
                            <span>Add Employee</span>
                        </a>
                    </div>
                    <div class="nav-item">
                        <a href="adm-emp-list.py" class="nav-link active">
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

    <div class="main-content">
        <div class="employee-table-container">
            <form action="" name="profile" method="post" enctype="multipart/form-data">
                <!-- Fixed header section -->
                <div class="table-header-container">
                    <div class="table-header">
                        <h2><i class="fas fa-users"></i> Employee List</h2>
                        <div class="quick-actions">
                            <a href="adm-emp-addform.py" class="quick-action-btn">
                                <i class="fas fa-user-plus"></i>
                                <span>Add Employee</span>
                            </a>
                        </div>
                    </div>

                    <div class="search-filter">
                        <!-- Your search filters here if needed -->
                    </div>
                </div>

                <!-- Scrollable table section -->
                <div class="scrollable-table-container">
                    <table class="employee-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Email_id</th>
                                <th>Phone</th>
                                <th>dob</th>
                                <th>gender</th>
                                <th>address</th>
                                <th>city</th>
                                <th>state</th>
                                <th>pincode</th>
                                <th>Empid</th>
                                <th>join_date</th>
                                <th>department</th>
                                <th>position</th>
                                <th>salary</th>
                                <th>shift</th>
                                <th>user_name</th>
                                <th>password</th>
                                <th>confirm_password</th>
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
        <td>{i[17]}</td>
        <td>{i[18]}</td>
    </tr>
    """)

print("""
                        </tbody>
                    </table>
                </div>

               
                   
                </div>
            </form>
        </div>
    </div>
</body>
</html>
""")

con.commit()
con.close()