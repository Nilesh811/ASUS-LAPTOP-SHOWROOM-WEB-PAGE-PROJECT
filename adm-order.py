#!C:/Python/python.exe

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymysql
import cgi, cgitb, os

cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

q = """select * from booking"""
cur.execute(q)
rec = cur.fetchall()
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Orders</title>
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

        /* Orders Section Styles */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }

        .page-header h1 {
            color: var(--asus-gray);
            font-size: 28px;
            font-weight: 600;
        }

        .page-header h1 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .search-filter {
            display: flex;
            gap: 15px;
        }

        .search-box {
            position: relative;
        }

        .search-box input {
            padding: 10px 15px 10px 40px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 250px;
            transition: all 0.3s;
        }

        .search-box input:focus {
            border-color: var(--asus-red);
            outline: none;
            box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.1);
        }

        .search-box i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #777;
        }

        .filter-dropdown select {
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
            cursor: pointer;
        }

        .filter-dropdown select:focus {
            border-color: var(--asus-red);
            outline: none;
        }

        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            overflow: hidden;
        }

        .card-header {
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header h3 {
            font-size: 18px;
            font-weight: 600;
            color: var(--asus-gray);
            margin: 0;
        }

        .card-header .badge {
            background-color: var(--asus-red);
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .table-responsive {
            overflow-x: auto;
        }

        .orders-table {
            width: 100%;
            border-collapse: collapse;
        }

        .orders-table th {
            background-color: #f5f5f5;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            color: var(--asus-gray);
            border-bottom: 2px solid #eee;
        }

        .orders-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
        }

        .orders-table tr:hover {
            background-color: #f9f9f9;
        }

        .order-id {
            color: var(--asus-red);
            font-weight: 600;
        }

        .customer-name {
            font-weight: 500;
        }

        .product-info {
            display: flex;
            align-items: center;
        }

        .product-img {
            width: 40px;
            height: 40px;
            border-radius: 4px;
            margin-right: 10px;
            object-fit: cover;
        }

        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .status-pending {
            background-color: #FFF3CD;
            color: #856404;
        }

        .status-processing {
            background-color: #CCE5FF;
            color: #004085;
        }

        .status-shipped {
            background-color: #D4EDDA;
            color: #155724;
        }

        .status-delivered {
            background-color: #D1ECF1;
            color: #0C5460;
        }

        .status-cancelled {
            background-color: #F8D7DA;
            color: #721C24;
        }

        .action-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            background-color: var(--asus-red);
            color: white;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.3s;
        }

        .action-btn:hover {
            background-color: #cc0000;
            transform: translateY(-1px);
        }

        .action-btn.view {
            background-color: var(--info);
        }

        .action-btn.view:hover {
            background-color: #0b7dda;
        }

        .action-btn.edit {
            background-color: var(--warning);
        }

        .action-btn.edit:hover {
            background-color: #e68a00;
        }

        .action-btn.delete {
            background-color: var(--negative);
        }

        .action-btn.delete:hover {
            background-color: #d32f2f;
        }

        .pagination {
            display: flex;
            justify-content: flex-end;
            padding: 15px 20px;
            border-top: 1px solid #eee;
        }

        .pagination button {
            padding: 8px 12px;
            margin: 0 5px;
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .pagination button:hover {
            background-color: #f5f5f5;
        }

        .pagination button.active {
            background-color: var(--asus-red);
            color: white;
            border-color: var(--asus-red);
        }

        .stats-cards {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
        }

        .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 20px;
        }

        .stat-icon.total {
            background-color: rgba(0, 123, 255, 0.1);
            color: #007BFF;
        }

        .stat-icon.pending {
            background-color: rgba(255, 193, 7, 0.1);
            color: #FFC107;
        }

        .stat-icon.completed {
            background-color: rgba(40, 167, 69, 0.1);
            color: #28A745;
        }

        .stat-icon.revenue {
            background-color: rgba(220, 53, 69, 0.1);
            color: #DC3545;
        }

        .stat-info h3 {
            font-size: 14px;
            color: #6C757D;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .stat-info h2 {
            font-size: 24px;
            color: var(--asus-gray);
            margin: 0;
            font-weight: 600;
        }

        @media (max-width: 1200px) {
            .stats-cards {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .stats-cards {
                grid-template-columns: 1fr;
            }

            .search-filter {
                flex-direction: column;
                width: 100%;
            }

            .search-box input {
                width: 100%;
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
                <a href="adm-emp-inventory.py" class="nav-link">
                    <i class="fas fa-laptop"></i>
                    <span>Inventory</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="adm-order.py" class="nav-link active">
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
        <div class="page-header">
            <h1><i class="fas fa-shopping-cart"></i> Orders Management</h1>
            <div class="search-filter">
               
                
            </div>
        </div>

     

        <div class="card">
            <div class="card-header">
                <h3>Recent Orders</h3>
                
            </div>
            <div class="table-responsive">
                <table class="orders-table">
                   <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Email_id</th>
                                <th>Phone</th>
                                <th>Address</th>
                                <th>Laptop_selection</th>
                                <th>Booking_date</th>
                              
                            </tr>
        """)
for i in rec:
    print("""
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
         <td>%s</td>
   
        </tr>"""%(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
print("""

                        </tbody>
                        </table>
            </div>
            <!-- <div class="pagination">
                <button><i class="fas fa-angle-double-left"></i></button>
                <button>1</button>
                <button class="active">2</button>
                <button>3</button>
                <button>4</button>
                <button><i class="fas fa-angle-double-right"></i></button>
            </div> -->
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
    </script>
</body>

</html>
      """)