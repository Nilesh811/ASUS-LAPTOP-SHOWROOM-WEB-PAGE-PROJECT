#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql

# Enable debugging
cgitb.enable()
form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()
pid = form.getvalue("id")

# Use parameterized query to prevent SQL injection
q = "SELECT * FROM `adm_emp_addform` WHERE id = %s"
cur.execute(q, (pid,))  # Execute the query with parameter
rec = cur.fetchone()  # Fetch one record since we're querying by ID

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-type:text/html\r\n\r\n")
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ASUS Showroom Employee Dashboard</title>
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

        .main-content {
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 25px;
            transition: all var(--transition-speed);
            position: relative;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Dashboard Cards */
        .dashboard-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .card-icon.sales {
            background-color: var(--asus-red);
        }

        .card-icon.customers {
            background-color: var(--info);
        }

        .card-icon.inventory {
            background-color: var(--warning);
        }

        .card-icon.target {
            background-color: var(--positive);
        }

        .card h3 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .card p {
            color: #666;
            font-size: 0.9rem;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        th,
        td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: var(--asus-gray);
            color: white;
            font-weight: 500;
        }

        tr:hover {
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

        .status-instock {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
        }

        .status-lowstock {
            background-color: rgba(255, 152, 0, 0.1);
            color: var(--warning);
        }

        .status-outstock {
            background-color: rgba(244, 67, 54, 0.1);
            color: var(--negative);
        }

        /* Charts Container */
        .charts-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }

        .chart-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .chart-card h3 {
            margin-bottom: 15px;
            color: var(--asus-gray);
        }

        .chart-placeholder {
            height: 250px;
            background: #f9f9f9;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            border-radius: 4px;
        }

        /* Form Styles */
        .form-container {
            max-width: 600px;
            margin: 20px auto;
            padding: 25px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .form-control {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }

        textarea.form-control {
            min-height: 100px;
            resize: vertical;
        }

        .btn {
            padding: 10px 20px;
            background-color: var(--asus-red);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        .btn:hover {
            background-color: #cc0000;
        }

        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        .alert-success {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
            border: 1px solid rgba(76, 175, 80, 0.2);
        }

        /* Responsive */
        @media (max-width: 1200px) {
            .charts-container {
                grid-template-columns: 1fr;
            }
        }

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
        }

        /* Welcome Section with Employee Info */
        .welcome-section {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.03);
        }

        .welcome-text {
            flex: 1;
            padding-right: 20px;
        }

        .welcome-text h1 {
            color: var(--asus-gray);
            margin-bottom: 10px;
            font-size: 2rem;
            position: relative;
            display: inline-block;
        }

        .welcome-text h1::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 50px;
            height: 3px;
            background: var(--asus-red);
        }

        .welcome-text p {
            color: #666;
            max-width: 600px;
            line-height: 1.6;
        }

        /* Employee Info Card */
        .employee-info-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            width: 350px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            border-left: 4px solid var(--asus-red);
            animation: float 4s ease-in-out infinite;
        }

        .employee-info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        }

        .employee-avatar {
            position: absolute;
            top: 20px;
            right: 20px;
            color: var(--asus-red);
            opacity: 0.2;
            font-size: 60px;
        }

        .employee-details {
            position: relative;
            z-index: 2;
        }

        .employee-name {
            color: var(--asus-gray);
            margin: 0 0 5px 0;
            font-size: 1.5rem;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }

        .employee-position {
            color: #666;
            margin: 0 0 15px 0;
            font-size: 1rem;
            font-style: italic;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }

        .employee-stats {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }

        .stat-item {
            text-align: center;
            padding: 8px 12px;
            background: rgba(0, 0, 0, 0.02);
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .stat-item:hover {
            background: rgba(255, 0, 0, 0.05);
            transform: scale(1.05);
        }

        .stat-value {
            display: block;
            font-weight: 700;
            color: var(--asus-red);
            font-size: 1.2rem;
        }

        .stat-label {
            display: block;
            font-size: 0.8rem;
            color: #666;
            margin-top: 3px;
        }

        .employee-status-indicator {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--asus-red), #ff6666);
            animation: pulse 2s infinite;
        }

        /* Animations */
        @keyframes float {
            0% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-8px);
            }
            100% {
                transform: translateY(0px);
            }
        }

        @keyframes pulse {
            0% {
                opacity: 0.8;
                width: 100%;
            }
            50% {
                opacity: 0.3;
                width: 95%;
            }
            100% {
                opacity: 0.8;
                width: 100%;
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

        <!-- Dashboard Section -->
        <section id="dashboard" class="tab-content active">
            <!-- Welcome Section with Employee Info -->
            <div class="welcome-section">
                <div class="welcome-text">
                    <h1>ASUS Showroom Dashboard</h1>
                    <p>Welcome to your showroom management dashboard. Track sales, inventory, and customer interactions.</p>
                </div>

                <!-- Enhanced Employee Info Card -->
                <div class="employee-info-card">
                    <i class="fas fa-user employee-avatar"></i>
                    <div class="employee-details">
                        <h1 class="employee-name">""")
print(rec[1] if rec else "Employee Name")
print("""</h1>
                        <p class="employee-position">""")
print(rec[13] if rec else "Position")
print("""</p>
                        <div class="employee-stats">
                            <div class="stat-item">
                                <span class="stat-value">ID: """)
print(pid if pid else "N/A")
print("""</span>
                            </div>
                        </div>
                    </div>
                    <div class="employee-status-indicator"></div>
                </div>
            </div>

         
        </section>
    </div>

<script>
    function toggleDropdown(el) {
        const dropdownMenu = el.nextElementSibling;

        // Close all other dropdowns
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            if (menu !== dropdownMenu) {
                menu.classList.remove('show');
                menu.previousElementSibling.classList.remove('active');
            }
        });

        el.classList.toggle('active');
        dropdownMenu.classList.toggle('show');
    }

    document.addEventListener('click', function (event) {
        if (!event.target.matches('.dropdown-toggle') && !event.target.closest('.dropdown-menu')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.classList.remove('active');
            });
        }
    });
    
</script>


</body>

</html>
""")