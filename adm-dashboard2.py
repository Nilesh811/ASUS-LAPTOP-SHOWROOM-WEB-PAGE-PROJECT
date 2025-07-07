#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql
from pymysql.err import ProgrammingError

# Enable debugging and set UTF-8 output
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("Content-type:text/html; charset=utf-8\r\n\r\n")

# Database connection with error handling
try:
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="final_laptopproject"
    )
    cur = con.cursor()

    # Get counts with error handling for missing tables
    def get_count(table_name, default=0):
        try:
            cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            return cur.fetchone()[0]
        except ProgrammingError as e:
            if "doesn't exist" in str(e):
                return default
            raise

    add_form = get_count("adm_emp_addform")
    inventory_form = get_count("emp_inv_addform")
    booking = get_count("booking")

    # HTML Template with escaped CSS curly braces
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin</title>
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
            left: 0;
            top: 0;
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
            padding-left: 0;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 0 0 8px 8px;
            display: block;
        }

        .dropdown-menu.show {
            max-height: 500px;
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
            padding: 20px;
            transition: all var(--transition-speed) ease;
            min-height: 100vh;
            background-color: #f9f9f9;
        }

        /* Dashboard Styles */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .page-title h1 {
            color: var(--asus-gray);
            font-size: 1.8rem;
            margin-bottom: 5px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .page-title p {
            color: #666;
            font-size: 0.9rem;
        }

        .user-actions {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .notification-bell {
            position: relative;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .notification-bell:hover {
            transform: scale(1.1);
        }

        .notification-bell:active {
            transform: scale(0.95);
        }

        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background-color: var(--asus-red);
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7);
            }

            70% {
                transform: scale(1.05);
                box-shadow: 0 0 0 10px rgba(255, 0, 0, 0);
            }

            100% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
            }
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            padding: 5px 10px;
            border-radius: 20px;
        }

        .user-profile:hover {
            background: rgba(0, 0, 0, 0.05);
        }

        .user-profile img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--asus-red);
            transition: all 0.3s ease;
        }

        .user-profile:hover img {
            transform: rotate(5deg);
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        }

        .user-info h4 {
            font-size: 0.9rem;
            font-weight: 600;
        }

        .user-info p {
            font-size: 0.8rem;
            color: #666;
        }

        /* Dashboard Widgets with ASUS Styling */
        .dashboard-widgets {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .widget {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            animation: slideUp 0.5s ease;
            position: relative;
            overflow: hidden;
        }

        .widget:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }

        .widget::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: var(--asus-red);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }

        .widget:hover::before {
            transform: scaleX(1);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .widget-header {
            display: flex;
            justify-content: space-between;
        }

        .widget-title {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .widget-value {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 5px;
            color: var(--asus-gray);
            font-family: 'Arial', sans-serif;
        }

        .widget-change {
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .widget-change.positive {
            color: var(--positive);
        }

        .widget-change.negative {
            color: var(--negative);
        }

        .widget-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            transition: all 0.3s ease;
        }

        .widget:hover .widget-icon {
            transform: scale(1.1) rotate(5deg);
        }

        .widget-icon.sales {
            background-color: rgba(255, 0, 0, 0.1);
            color: var(--asus-red);
        }

        .widget-icon.inventory {
            background-color: rgba(0, 0, 0, 0.1);
            color: var(--asus-black);
        }

        .widget-icon.customers {
            background-color: rgba(33, 150, 243, 0.1);
            color: var(--info);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
                overflow: hidden;
            }

            .sidebar-header h3,
            .nav-link span,
            .dropdown-toggle::after {
                display: none;
            }

            .sidebar-header {
                justify-content: center;
                padding: 20px 0;
            }

            .sidebar-header img {
                margin-right: 0;
            }

            .nav-link {
                justify-content: center;
                padding: 15px 0;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.3rem;
            }

            .dropdown-menu {
                display: none;
            }

            .sidebar:not(.collapsed) .dropdown-menu {
                display: block;
            }

            .sidebar.collapsed .dropdown-menu {
                display: none;
            }

            .main-content {
                margin-left: var(--sidebar-collapsed-width);
                width: calc(100% - var(--sidebar-collapsed-width));
            }

            .dashboard-widgets {
                grid-template-columns: 1fr;
            }
        }

        /* Toggle Sidebar Animation */
        .sidebar.collapsed {
            width: var(--sidebar-collapsed-width);
        }

        .sidebar.collapsed .sidebar-header h3,
        .sidebar.collapsed .nav-link span,
        .sidebar.collapsed .dropdown-toggle::after {
            display: none;
        }

        .sidebar.collapsed .sidebar-header {
            justify-content: center;
            padding: 20px 0;
        }

        .sidebar.collapsed .sidebar-header img {
            margin-right: 0;
        }

        .sidebar.collapsed .nav-link {
            justify-content: center;
            padding: 15px 0;
        }

        .sidebar.collapsed .nav-link i {
            margin-right: 0;
            font-size: 1.3rem;
        }

        .sidebar.collapsed .dropdown-menu {
            display: none;
        }

        .main-content.expanded {
            margin-left: var(--sidebar-collapsed-width);
            width: calc(100% - var(--sidebar-collapsed-width));
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
                        <a href="adm-emp-addform.py" class="nav-link active">
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
    <!-- Main Content Area -->
    <div class="main-content">
        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <!-- Top Navigation -->
            <div class="top-nav">
                <div class="page-title">
                    <h1>ADMIN Dashboard</h1>
                    <p>Welcome back, Administrator. Here's what's happening with your showroom today.</p>
                </div>
               
                    <div class="user-profile">
                        <img src="./img/1000038538.jpg" alt="User">
                        <div class="user-info">
                            <h4>NILESH</h4>
                            <p>OWNER</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dashboard Widgets -->
            <div class="dashboard-widgets">
                <div class="widget">
                    <div class="widget-header">
                        <div>
                            <div class="widget-title">Total Employees</div>
                            <div class="widget-value">{add_form}</div>
                        </div>
                    </div>
                </div>
                <div class="widget">
                    <div class="widget-header">
                        <div>
                            <div class="widget-title">Inventory Items</div>
                            <div class="widget-value">{inventory_form}</div>
                        </div>
                    </div>
                </div>
                <div class="widget">
                    <div class="widget-header">
                        <div>
                            <div class="widget-title">Total Bookings</div>
                            <div class="widget-value">{booking}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Wait for DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Dropdown functionality
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

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

            // Close dropdowns when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.nav-item')) {
                    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                        toggle.classList.remove('active');
                        toggle.nextElementSibling.classList.remove('show');
                    });
                }
            });

            // Set active link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', function(e) {
                    if (!this.classList.contains('dropdown-toggle')) {
                        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                        this.classList.add('active');

                        // If this is inside a dropdown, make parent link active too
                        let parentItem = this.closest('.dropdown-menu');
                        if (parentItem) {
                            parentItem.previousElementSibling.classList.add('active');
                        }
                    }
                });
            });

            // Notification bell click event
            document.querySelector('.notification-bell').addEventListener('click', function() {
                this.querySelector('.notification-badge').style.animation = 'none';
                setTimeout(() => {
                    this.querySelector('.notification-badge').style.animation = 'pulse 2s infinite';
                }, 10);

                alert('You have 3 new notifications:\n\n1. New order #ASUS-8453\n2. Inventory alert: ROG Zephyrus low stock\n3. System update available');
            });

            // Toggle sidebar (for demo purposes)
            document.addEventListener('keydown', function(e) {
                if (e.key === 't' || e.key === 'T') {
                    document.querySelector('.sidebar').classList.toggle('collapsed');
                    document.querySelector('.main-content').classList.toggle('expanded');
                }
            });
        });
    </script>
</body>
</html>"""

    # Safely format the HTML (using replace instead of format to avoid CSS issues)
    html_output = html_template.replace("{add_form}", str(add_form)) \
                              .replace("{inventory_form}", str(inventory_form)) \
                              .replace("{booking}", str(booking))

    print(html_output)

except Exception as e:
    print(f"<h1>Error</h1><p>{str(e)}</p>")
    # For debugging - remove in production
    raise

finally:
    # Clean up database connections
    if 'cur' in locals():
        cur.close()
    if 'con' in locals():
        con.close()