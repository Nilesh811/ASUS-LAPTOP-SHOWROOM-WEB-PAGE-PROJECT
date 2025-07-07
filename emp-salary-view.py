#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql

form = cgi.FieldStorage()
cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()
pid = form.getvalue("id")

q = """select * from salary_table where id =%s""" % (pid)
cur.execute(q)
rec = cur.fetchall()

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-type:text/html\r\n\r\n")
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ASUS Showroom - Salary View</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');

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
            padding: 30px;
            transition: all var(--transition-speed) ease;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: var(--asus-gray);
            font-size: 2rem;
            font-weight: 700;
        }

        .header h1 span {
            color: var(--asus-red);
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .user-profile img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }

        .user-profile span {
            font-weight: 600;
            color: var(--asus-gray);
        }

        /* Salary Table */
        .salary-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 25px;
            margin-bottom: 30px;
        }

        .salary-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .salary-header h2 {
            color: var(--asus-gray);
            font-size: 1.5rem;
        }

        .table-responsive {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            max-width: 100%;
            border: 1px solid #eee;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        .table-responsive::-webkit-scrollbar {
            height: 8px;
        }

        .table-responsive::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 4px;
        }

        .table-responsive::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 1000px;
        }

        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
            white-space: nowrap;
        }

        th {
            background-color: var(--asus-light);
            color: var(--asus-gray);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
            position: sticky;
            top: 0;
        }

        tr:hover {
            background-color: rgba(255, 0, 0, 0.03);
        }

        .status {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .status-paid {
            background-color: rgba(76, 175, 80, 0.1);
            color: var(--positive);
        }

        .status-pending {
            background-color: rgba(255, 152, 0, 0.1);
            color: var(--warning);
        }

        .salary-amount {
            font-weight: 700;
            color: var(--asus-gray);
        }

        .action-btn {
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .view-btn {
            background-color: var(--info);
            color: white;
        }

        .view-btn:hover {
            background-color: #0d8bf2;
        }

        .download-btn {
            background-color: var(--positive);
            color: white;
            margin-left: 10px;
        }

        .download-btn:hover {
            background-color: #3d9a4a;
        }

        /* Summary Cards */
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
        }

        .summary-card h3 {
            color: var(--asus-gray);
            font-size: 1rem;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .summary-card .amount {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--asus-black);
            margin-bottom: 5px;
        }

        .summary-card .info {
            font-size: 0.9rem;
            color: #666;
        }

        .card-red {
            border-left: 4px solid var(--asus-red);
        }

        .card-green {
            border-left: 4px solid var(--positive);
        }

        .card-blue {
            border-left: 4px solid var(--info);
        }

        /* Responsive */
        @media (max-width: 992px) {
            .summary-cards {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 80px;
                overflow: hidden;
            }

            .sidebar-header h3, 
            .nav-link span, 
            .dropdown-toggle span {
                display: none;
            }

            .sidebar-header {
                justify-content: center;
            }

            .nav-link {
                justify-content: center;
                padding: 12px 0;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.3rem;
            }

            .main-content {
                margin-left: 80px;
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
        <div class="header">
            <h1>Salary <span>History</span></h1>
        </div>

        <!-- Salary Table -->
        <div class="salary-container">
            <div class="salary-header">
                <h2>Salary Transactions</h2>
            </div>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>emp_id</th>
                            <th>emp_name</th>
                            <th>Email_Id</th>
                            <th>month</th>
                            <th>year</th>
                            <th>salary Card</th>
                            <th>wdays</th>
                            <th>pdays</th>
                            <th>leave_taken</th>
                            <th>gross_salary</th>
                        </tr>
                    </thead>
                    <tbody>
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
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]))

print("""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Toggle dropdown functionality
        function toggleDropdown(element) {
            // Get the next sibling (the dropdown menu)
            const dropdownMenu = element.nextElementSibling;

            // Close all other dropdowns first
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu !== dropdownMenu) {
                    menu.classList.remove('show');
                }
            });

            // Toggle the clicked dropdown
            dropdownMenu.classList.toggle('show');
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.nav-item')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    </script>
</body>

</html>
""")