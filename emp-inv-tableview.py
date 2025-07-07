#!C:/Python/python.exe

# Fix encoding issues
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-type:text/html; charset=utf-8\r\n\r\n")

import pymysql
import cgi, cgitb, os

cgitb.enable()
form = cgi.FieldStorage()
pid = form.getvalue("id")
cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

# Fix: Add backticks around the table name
q = """select * from `emp_inv_addform`where id =%s""" %(pid)
cur.execute(q)
rec = cur.fetchall()
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ASUS Showroom - Inventory List</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');

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
            --transition-speed: 0.3s;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            display: flex;
            min-height: 100vh;
            background-color: #f9f9f9;
            overflow-x: hidden;
        }

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

        /* Main Content */
        .main-content {
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 25px;
            transition: all var(--transition-speed);
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }

        .page-title {
            font-size: 1.8rem;
            color: var(--asus-gray);
            font-weight: 700;
        }

        .page-title span {
            color: var(--asus-red);
        }

        /* Inventory Table Styles */
        .inventory-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            padding: 30px;
            animation: fadeIn 0.5s ease;
        }

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

        .inventory-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .inventory-header h3 {
            font-size: 1.4rem;
            color: var(--asus-gray);
            display: flex;
            align-items: center;
        }

        .inventory-header h3 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .search-box {
            position: relative;
            width: 300px;
        }

        .search-box input {
            width: 100%;
            padding: 10px 15px 10px 40px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
            transition: all var(--transition-speed) ease;
        }

        .search-box input:focus {
            border-color: var(--asus-red);
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
            outline: none;
        }

        .search-box i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--asus-gray);
        }

        .table-responsive {
            overflow-x: auto;
        }

        .inventory-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .inventory-table th,
        .inventory-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .inventory-table th {
            background-color: var(--asus-gray);
            color: white;
            font-weight: 500;
        }

        .inventory-table tr:hover {
            background-color: #f5f5f5;
        }

        .status {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .status-pending {
            background-color: rgba(255, 152, 0, 0.1);
            color: var(--warning);
        }

        .status-approved {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
        }

        .status-rejected {
            background-color: rgba(244, 67, 54, 0.1);
            color: var(--negative);
        }

        .btn {
            padding: 8px 15px;
            background-color: var(--asus-red);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
            display: inline-flex;
            align-items: center;
        }

        .btn i {
            margin-right: 5px;
        }

        .btn:hover {
            background-color: #cc0000;
        }

        /* Responsive */
        @media (max-width: 768px) {
            body {
                flex-direction: column;
            }

            .sidebar {
                width: 70px;
            }

            .sidebar-header h3,
            .nav-link span {
                display: none;
            }

            .nav-link {
                justify-content: center;
                padding: 15px 0;
            }

            .main-content {
                margin-left: 70px;
            }

            .inventory-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }

            .search-box {
                width: 100%;
            }

            .inventory-table {
                font-size: 0.9rem;
            }

            .inventory-table th,
            .inventory-table td {
                padding: 8px 10px;
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
                           """ % pid)
print("""
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
        <div class="page-header">
            <h1 class="page-title">Inventory <span>Management</span></h1>
            <a href="./emp-inventory.py?id=%s" class="btn">
                <i class="fas fa-plus"></i> Add Product
            </a>
        </div>

        <div class="inventory-container">
            <div class="inventory-header">
                <h3><i class="fas fa-laptop"></i> Current Inventory</h3>
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search products...">
                </div>
            </div>

            <div class="table-responsive">
                <table class="inventory-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Category</th>
                            <th>Laptop Model</th>
                            <th>Series</th>
                            <th>Processor</th>
                            <th>Graphics Card</th>
                            <th>RAM</th>
                            <th>Storage</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Features</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
""")

for i in rec:
    # Determine status class based on quantity
    quantity = int(i[9]) if i[9] else 0
    status_class = "status-approved" if quantity > 10 else "status-pending" if quantity > 0 else "status-rejected"
    status_text = "In Stock" if quantity > 10 else "Low Stock" if quantity > 0 else "Out of Stock"

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
        <td>₹{i[8]}</td>
        <td>{i[9]}</td>
        <td>{i[10]}</td>
        <td><span class="status {status_class}">{status_text}</span></td>
    </tr>""")

print("""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Dropdown toggle
        function toggleDropdown(el) {
            el.classList.toggle("active");
            const menu = el.nextElementSibling;
            menu.classList.toggle("show");
        }

        // Search functionality
        document.querySelector('.search-box input').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.inventory-table tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });

        // Highlight active link
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop();
            const links = document.querySelectorAll('.nav-link, .dropdown-menu a');

            links.forEach(link => {
                if (link.getAttribute('href').includes(currentPage)) {
                    link.classList.add('active');
                }
            });
        });
    </script>

</body>

</html>
""")
con.commit()
con.close()