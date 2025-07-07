#!C:/Python/python.exe
print("Content-type:text/html\r\n\r\n")

import pymysql
import cgi, cgitb
import os
import sys, io

# Enable debugging
cgitb.enable()

# Setup UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

# Corrected table name with backticks to escape the hyphens
q1 = """SELECT * FROM `adm_emp_addform`"""
cur.execute(q1)
res = cur.fetchall()

print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Salary Management</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
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
            height: calc(100vh - 80px);
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: var(--asus-red) var(--asus-black);
        }

        .nav-menu::-webkit-scrollbar {
            width: 5px;
        }

        .nav-menu::-webkit-scrollbar-track {
            background: var(--asus-black);
        }

        .nav-menu::-webkit-scrollbar-thumb {
            background-color: var(--asus-red);
            border-radius: 6px;
        }

        .nav-item {
            position: relative;
            margin: 0;
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

        .dropdown-container {
            position: relative;
        }

        .dropdown-menu {
            padding-left: 0;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease;
            background: rgba(20, 20, 20, 0.8);
            margin: 0;
            border-radius: 0;
            border: none;
            display: block;
            position: relative;
            width: 100%;
            box-shadow: none;
        }

        .dropdown-menu.show {
            max-height: 500px;
        }

        .dropdown-menu .nav-link {
            padding: 10px 20px 10px 55px;
            font-size: 0.9rem;
            background: transparent;
        }

        .dropdown-menu .nav-link:hover {
            background: rgba(255, 0, 0, 0.1);
        }

        .dropdown-menu .nav-link i {
            font-size: 0.9rem;
        }

        .dropdown-toggle {
            cursor: pointer;
            position: relative;
            user-select: none;
        }

        .dropdown-toggle::after {
            content: '\f078';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 20px;
            transition: all var(--transition-speed) ease;
            border: none;
            margin-left: 0;
            vertical-align: 0;
            font-size: 0.8rem;
        }

        .dropdown-toggle.active::after {
            transform: rotate(180deg);
            color: white;
        }

        .logout {
            margin-top: auto;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
            position: sticky;
            bottom: 0;
            background: var(--asus-black);
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

        /* Main Content Styles */
        .main-content {
            margin-left: var(--sidebar-width);
            padding: 30px;
            width: calc(100% - var(--sidebar-width));
            transition: all var(--transition-speed) ease;
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255, 0, 0, 0.1);
            animation: fadeInDown 0.5s ease;
        }

        .page-header h2 {
            color: var(--asus-gray);
            font-weight: 700;
            font-size: 1.8rem;
            position: relative;
        }

        .page-header h2::after {
            content: '';
            position: absolute;
            bottom: -17px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--asus-red);
        }

        .btn-asus {
            background-color: var(--asus-red);
            color: white;
            border: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .btn-asus:hover {
            background-color: #d90000;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
        }

        .btn-asus-outline {
            background-color: transparent;
            color: var(--asus-red);
            border: 1px solid var(--asus-red);
            transition: all 0.3s ease;
        }

        .btn-asus-outline:hover {
            background-color: var(--asus-red);
            color: white;
        }

        .table-responsive {
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            animation: fadeIn 0.6s ease;
        }

        .table {
            margin-bottom: 0;
            border-collapse: separate;
            border-spacing: 0;
        }

        .table th {
            background-color: var(--asus-black);
            color: white;
            font-weight: 600;
            border-bottom: 2px solid var(--asus-red);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .table td {
            vertical-align: middle;
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            transition: all 0.2s ease;
        }

        .table tr:hover td {
            background-color: rgba(255, 0, 0, 0.03);
            transform: translateX(3px);
        }

        .table tr:last-child td {
            border-bottom: none;
        }

        .leave-days {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            background-color: rgba(255, 152, 0, 0.1);
            color: var(--warning);
            font-size: 0.85rem;
            font-weight: 500;
        }

        .deduction-info {
            color: var(--negative);
            font-weight: 500;
        }

        .total-salary {
            font-weight: 700;
            color: var(--positive);
        }

        /* Responsive adjustments */
        @media (max-width: 992px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
            }

            .sidebar-header h3,
            .nav-link span {
                display: none;
            }

            .sidebar-header {
                justify-content: center;
                padding: 15px 0;
            }

            .sidebar-header img {
                margin-right: 0;
            }

            .nav-link {
                justify-content: center;
                padding: 12px 0;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.2rem;
            }

            .dropdown-toggle::after {
                display: none;
            }

            .dropdown-menu {
                position: absolute;
                left: 100%;
                top: 0;
                width: 200px;
                background: var(--asus-black);
                z-index: 1000;
                border-radius: 0 5px 5px 0;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }

            .dropdown-menu .nav-link {
                padding: 10px 15px;
                justify-content: flex-start;
            }

            .dropdown-menu .nav-link i {
                margin-right: 10px;
            }

            .main-content {
                margin-left: var(--sidebar-collapsed-width);
                width: calc(100% - var(--sidebar-collapsed-width));
            }
        }
    </style>
</head>

<body>
    <!-- Vertical Sidebar Navbar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            <h3>ASUS <span>Admin</span></h3>
        </div>

        <div class="nav-menu">
            <div class="nav-item">
                <a href="adm-dashboard2.py" class="nav-link">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </div>

            <div class="nav-item dropdown-container">
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
                <a href="adm-emp-lev.py" class="nav-link">
                    <i class="fas fa-calendar-minus"></i>
                    <span>Leave Requests</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="salary.py" class="nav-link active">
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
    </div>

    <div class="main-content">
        <div class="page-header">
            <h2>Employee Salary Management</h2>
        </div>

        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Emp ID</th>
                        <th>Email</th>
                        <th>Department</th>
                        <th>Position</th>
                        <th>Shift</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
""")

for i in res:
    print(f"""
                    <tr>
                        <td>{i[1]}</td>
                        <td>{i[10]}</td>
                        <td>{i[2]}</td>
                        <td>{i[12]}</td>
                        <td>{i[13]}</td>
                        <td>{i[15]}</td>
                        <td>
                            <a href="./salarycal.py?id={i[0]}" class="btn btn-asus btn-sm">Calculate Salary</a>
                        </td>
                    </tr>
    """)

print("""
                </tbody>
            </table>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Dropdown functionality
            const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

            dropdownToggles.forEach(toggle => {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    const parentItem = this.closest('.dropdown-container');
                    const menu = this.nextElementSibling;
                    const isActive = this.classList.contains('active');

                    // Close all other dropdowns first
                    document.querySelectorAll('.dropdown-menu').forEach(m => {
                        if (m !== menu) {
                            m.classList.remove('show');
                        }
                    });
                    document.querySelectorAll('.dropdown-toggle').forEach(t => {
                        if (t !== this) {
                            t.classList.remove('active');
                        }
                    });

                    // Toggle current dropdown
                    this.classList.toggle('active');
                    menu.classList.toggle('show');
                });
            });

            // Close dropdowns when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.dropdown-container')) {
                    document.querySelectorAll('.dropdown-menu').forEach(menu => {
                        menu.classList.remove('show');
                    });
                    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                        toggle.classList.remove('active');
                    });
                }
            });

            // Prevent dropdown from closing when clicking inside it
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });

            // Handle responsive behavior
            function handleResponsive() {
                const dropdownMenus = document.querySelectorAll('.dropdown-menu');
                const isMobile = window.innerWidth <= 992;

                dropdownMenus.forEach(menu => {
                    if (isMobile) {
                        menu.style.position = 'absolute';
                        menu.style.left = '100%';
                        menu.style.top = '0';
                        menu.style.width = '200px';
                    } else {
                        menu.style.position = 'relative';
                        menu.style.left = 'auto';
                        menu.style.top = 'auto';
                        menu.style.width = '100%';
                    }
                });
            }

            // Initial call and window resize listener
            handleResponsive();
            window.addEventListener('resize', handleResponsive);
        });
    </script>
</body>
</html>
""")

con.commit()
con.close()