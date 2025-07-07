#!C:/Python/python.exe
print("Content-type:text/html\r\n\r\n")

import pymysql
import cgi, cgitb, os
import sys, io

# Enable debugging
cgitb.enable()

# Setup UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

# Fetch pending laptop entries
q = """SELECT * FROM `emp_inv_addform` WHERE status='pending' """
cur.execute(q)
rec = cur.fetchall()

# Handle Accept/Decline
form = cgi.FieldStorage()
paccept = form.getvalue("accept")
pdecline = form.getvalue("decline")
pid = form.getvalue("id")

if paccept:
    q2 = """UPDATE `emp-inv-addform` SET status='approved' WHERE id='%s' """ % (pid)
    cur.execute(q2)
    con.commit()
    print("""
        <script>alert("Product approved successfully!"); window.location.href = "adm-emp-inventory.py";</script>
    """)

if pdecline:
    q2 = """UPDATE `emp-inv-addform` SET status='rejected' WHERE id='%s' """ % (pid)
    cur.execute(q2)
    con.commit()
    print("""
        <script>alert("Product rejected successfully!"); window.location.href = "adm-emp-inventory.py";</script>
    """)

# HTML Start
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Inventory Requests</title>
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
            background-color: #f5f5f5;
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
            box-shadow: 2px 0 20px rgba(255, 0, 0, 0.2);
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }

        .sidebar-header {
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transition: all var(--transition-speed) ease;
            background: rgba(255, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        .sidebar-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--asus-red);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.5s ease;
        }

        .sidebar:hover .sidebar-header::after {
            transform: scaleX(1);
        }

        .sidebar-header img {
            width: 40px;
            margin-right: 10px;
            transition: all var(--transition-speed) ease;
            filter: drop-shadow(0 0 5px rgba(255, 0, 0, 0.5));
        }

        .sidebar-header h3 {
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all var(--transition-speed) ease;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        }

        .sidebar-header span {
            color: var(--asus-red);
            font-weight: 700;
            text-shadow: 0 0 8px rgba(255, 0, 0, 0.5);
        }

        .nav-menu {
            padding: 20px 0;
            position: relative;
        }

        .nav-menu::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://www.asus.com/media/global/gallery/background_dots.png') center/cover;
            opacity: 0.05;
            pointer-events: none;
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
            z-index: 1;
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
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
        }

        .nav-link:hover i {
            transform: scale(1.2);
            color: white;
            filter: drop-shadow(0 0 5px rgba(255, 0, 0, 0.7));
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

        .nav-link::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.1), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
            z-index: -1;
        }

        .nav-link:hover::after {
            transform: translateX(100%);
        }

        .nav-link.active {
            background: rgba(255, 0, 0, 0.2);
            padding-left: 25px;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
        }

        .nav-link.active i {
            color: white;
            transform: scale(1.1);
            filter: drop-shadow(0 0 5px rgba(255, 0, 0, 0.7));
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

        /* Main Content Styles */
        .main-content {
            margin-left: var(--sidebar-width);
            width: calc(100% - var(--sidebar-width));
            padding: 30px;
            transition: all var(--transition-speed) ease;
            min-height: 100vh;
        }

        .container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }

        h2 {
            color: var(--asus-black);
            margin-bottom: 25px;
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h2 i {
            color: var(--asus-red);
        }

        .requests-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            overflow-x: auto;
        }

        .requests-table th, .requests-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }

        .requests-table th {
            background-color: var(--asus-black);
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
        }

        .requests-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .requests-table tr:hover {
            background-color: #f1f1f1;
        }

        .status-pending {
            background-color: var(--warning);
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .btn-success, .btn-danger {
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 2px;
        }

        .btn-success {
            background-color: var(--positive);
            color: white;
        }

        .btn-danger {
            background-color: var(--negative);
            color: white;
        }

        .btn-success:hover {
            background-color: #3e8e41;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .btn-danger:hover {
            background-color: #d32f2f;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Responsive Styles */
        @media (max-width: 992px) {
            .requests-table {
                display: block;
                overflow-x: auto;
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
            }

            .sidebar-header h3, .nav-link span {
                display: none;
            }

            .sidebar-header {
                justify-content: center;
                padding: 20px 10px;
            }

            .sidebar-header img {
                margin-right: 0;
            }

            .nav-link {
                justify-content: center;
                padding: 12px 10px;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.2rem;
            }

            .dropdown-toggle::after {
                display: none;
            }

            .dropdown-menu {
                position: fixed;
                left: var(--sidebar-collapsed-width);
                width: 200px;
                background: var(--asus-black);
                border-radius: 0 8px 8px 0;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);
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

        @media (max-width: 576px) {
            .container {
                padding: 15px;
            }

            h2 {
                font-size: 1.4rem;
            }

            .requests-table th, .requests-table td {
                padding: 8px 10px;
                font-size: 0.9rem;
            }

            .btn-success, .btn-danger {
                padding: 6px 10px;
                font-size: 0.8rem;
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
                <a href="adm-emp-inventory.py" class="nav-link active">
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
        <div class="container">
            <h2><i class="fas fa-clock"></i> ASUS Laptop Inventory Requests (Pending)</h2>
            <table class="requests-table">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Model</th>
                        <th>Series</th>
                        <th>Processor</th>
                        <th>Graphics Card</th>
                        <th>RAM</th>
                        <th>Storage</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Additional Features</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
""")

# Loop through records
for i in rec:
    print("""
                    <tr>
                    <form method="post">
                        <input type="hidden" name="id" value="%s">
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td><span class="status-pending">%s</span></td>
                        <td>
                            <input class="btn-success" type="submit" name="accept" value="Accept">
                            <input class="btn-danger" type="submit" name="decline" value="Decline">
                        </td>
                    </form>
                    </tr>
    """ % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]))

print("""
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Dropdown functionality
        document.addEventListener('DOMContentLoaded', function() {
            const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

            dropdownToggles.forEach(toggle => {
                toggle.addEventListener('click', function() {
                    const dropdownMenu = this.nextElementSibling;
                    this.classList.toggle('active');
                    dropdownMenu.classList.toggle('show');
                });
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.nav-item')) {
                    document.querySelectorAll('.dropdown-menu').forEach(menu => {
                        menu.classList.remove('show');
                    });
                    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                        toggle.classList.remove('active');
                    });
                }
            });

            // Responsive sidebar toggle
            const sidebar = document.querySelector('.sidebar');
            const mainContent = document.querySelector('.main-content');
            const sidebarWidth = getComputedStyle(document.documentElement).getPropertyValue('--sidebar-width');
            const sidebarCollapsedWidth = getComputedStyle(document.documentElement).getPropertyValue('--sidebar-collapsed-width');

            function handleResize() {
                if (window.innerWidth <= 768) {
                    sidebar.style.width = sidebarCollapsedWidth;
                    mainContent.style.marginLeft = sidebarCollapsedWidth;
                } else {
                    sidebar.style.width = sidebarWidth;
                    mainContent.style.marginLeft = sidebarWidth;
                }
            }

            // Initialize on load
            handleResize();

            // Add resize listener
            window.addEventListener('resize', handleResize);
        });
    </script>
</body>
</html>
""")

# Close DB
con.close()