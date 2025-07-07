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

q = """select * from employee_leave_form where id =%s""" %(pid)
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
    <title>ASUS Showroom - Leave History</title>
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

        /* Sidebar - Same as before */
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
            margin-left: var(--sidebar-width);
            padding: 30px;
            width: calc(100% - var(--sidebar-width));
            min-height: 100vh;
        }

        /* Header */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
            animation: fadeInDown 0.6s;
        }

        .page-header h1 {
            color: var(--asus-gray);
            font-size: 1.8rem;
        }

        .page-header h1 span {
            color: var(--asus-red);
        }

        .user-profile {
            display: flex;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s;
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
            margin-right: 10px;
            border: 2px solid var(--asus-red);
            object-fit: cover;
        }

        /* Leave History Styles */
        .leave-history-container {
            max-width: 1200px;
            margin: 20px auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            animation: fadeIn 0.8s;
            transform-origin: top;
        }

        .history-header {
            padding: 20px 25px;
            background: var(--asus-black);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        .history-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 65%, rgba(255, 0, 0, 0.1) 100%);
            z-index: 0;
        }

        .history-header h2 {
            font-size: 1.4rem;
            position: relative;
            z-index: 1;
        }

        .history-header h2 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .filter-controls {
            display: flex;
            gap: 15px;
            position: relative;
            z-index: 1;
        }

        .filter-controls select,
        .filter-controls input {
            padding: 8px 15px;
            border-radius: 4px;
            border: none;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: all 0.3s;
        }

        .filter-controls select:focus,
        .filter-controls input:focus {
            outline: none;
            box-shadow: 0 0 0 2px var(--asus-red);
        }

        .history-table-container {
            overflow-x: auto;
            padding: 0 5px;
        }

        .history-table {
            width: 100%;
            border-collapse: collapse;
            min-width: 800px;
        }

        .history-table th {
            background-color: #f5f5f5;
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            color: var(--asus-gray);
            border-bottom: 2px solid #eee;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .history-table td {
            padding: 15px;
            border-bottom: 1px solid #eee;
            vertical-align: middle;
            transition: all 0.3s;
        }

        .history-table tr {
            transition: all 0.3s;
        }

        .history-table tr:not(:first-child) {
            animation: fadeInUp 0.5s;
            animation-fill-mode: both;
        }

        .history-table tr:nth-child(1) {
            animation-delay: 0.1s;
        }

        .history-table tr:nth-child(2) {
            animation-delay: 0.2s;
        }

        .history-table tr:nth-child(3) {
            animation-delay: 0.3s;
        }

        .history-table tr:nth-child(4) {
            animation-delay: 0.4s;
        }

        .history-table tr:nth-child(5) {
            animation-delay: 0.5s;
        }

        .history-table tr:last-child td {
            border-bottom: none;
        }

        .history-table tr:hover {
            background-color: rgba(255, 0, 0, 0.03);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }

        .history-table tr:hover td {
            color: var(--asus-gray);
        }

        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: all 0.3s;
        }

        .status-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .status-approved {
            background-color: rgba(76, 175, 80, 0.15);
            color: var(--positive);
            border: 1px solid rgba(76, 175, 80, 0.3);
        }

        .status-declined {
            background-color: rgba(244, 67, 54, 0.15);
            color: var(--negative);
            border: 1px solid rgba(244, 67, 54, 0.3);
        }

        .status-pending {
            background-color: rgba(255, 152, 0, 0.15);
            color: var(--warning);
            border: 1px solid rgba(255, 152, 0, 0.3);
        }

        .action-btn {
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            background: var(--asus-red);
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .action-btn:hover {
            background: #cc0000;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .action-btn i {
            font-size: 0.9rem;
        }

        .pagination {
            display: flex;
            justify-content: center;
            padding: 25px;
            background: #f5f5f5;
            border-top: 1px solid #eee;
        }

        .pagination button {
            padding: 10px 16px;
            margin: 0 5px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
            min-width: 40px;
        }

        .pagination button:hover:not(:disabled) {
            background: var(--asus-red);
            color: white;
            border-color: var(--asus-red);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .pagination button.active {
            background: var(--asus-red);
            color: white;
            border-color: var(--asus-red);
        }

        .pagination button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Modal Styles */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
            backdrop-filter: blur(5px);
        }

        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 8px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow: auto;
            transform: translateY(-50px);
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            border-top: 4px solid var(--asus-red);
        }

        .modal-overlay.active .modal-content {
            transform: translateY(0);
        }

        .modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--asus-gray);
            transition: all 0.3s;
        }

        .modal-close:hover {
            color: var(--asus-red);
            transform: rotate(90deg);
        }

        .modal-title {
            margin-bottom: 20px;
            color: var(--asus-gray);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .modal-title i {
            color: var(--asus-red);
        }

        .detail-item {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px dashed #eee;
            display: flex;
        }

        .detail-item:last-child {
            border-bottom: none;
        }

        .detail-label {
            font-weight: 600;
            color: var(--asus-gray);
            min-width: 150px;
        }

        .detail-value {
            flex: 1;
        }

        /* Responsive Styles */
        @media (max-width: 992px) {
            .main-content {
                padding: 20px;
            }

            .history-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
                padding: 15px;
            }

            .filter-controls {
                width: 100%;
                flex-wrap: wrap;
            }

            .filter-controls select,
            .filter-controls input {
                flex: 1 1 200px;
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }

            .main-content {
                margin-left: 0;
                width: 100%;
            }

            .detail-item {
                flex-direction: column;
                gap: 5px;
            }

            .detail-label {
                min-width: 100%;
            }
        }

        /* Animations */
        @keyframes pulse {
            0% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.05);
            }

            100% {
                transform: scale(1);
            }
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--asus-red);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #cc0000;
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
            <h1>Leave <span>History</span></h1>

        </div>

        <div class="leave-history-container">
            <div class="history-header">
                <h2><i class="fas fa-history pulse"></i> Your Leave Requests</h2>
                <div class="filter-controls">


                </div>
            </div>

            <div class="history-table-container">
                <table class="history-table">
                   <thead>
                            <tr>
                                <th>#</th>
                                <th>Employee_id</th>
                                <th>Employee_name</th>
                                <th>department</th>
                                <th>position</th>
                                <th>leave_type</th>
                                <th>days_requested</th>
                                <th>from_date</th>
                                <th>to_date</th>
                                <th>reason</th>
                                <th>status</th>                            
                            </tr>
                            """)

for i in rec:
    # Determine the CSS class based on status
    status_class = ""
    if i[10].lower() == "approved":
        status_class = "status-approved"
    elif i[10].lower() == "declined":
        status_class = "status-declined"
    else:
        status_class = "status-pending"

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
        <td><span class="status-badge %s">%s</span></td>
    </tr>""" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], status_class, i[10]))
print("""

                        </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Modal for leave details -->
    <div class="modal-overlay" id="leaveDetailsModal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <h2 class="modal-title"><i class="fas fa-file-alt"></i> Leave Request Details</h2>
            <div id="leaveDetailsContent">
                <!-- Details will be loaded here -->
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

        // Modal functions
        function openModal(leaveId) {
            // Here you would typically fetch the leave details using AJAX
            // For now, we'll just show the modal
            document.getElementById('leaveDetailsModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('leaveDetailsModal').classList.remove('active');
        }

        // Close modal when clicking outside
        document.getElementById('leaveDetailsModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    </script>
</body>

</html>
""")
con.commit()
con.close()