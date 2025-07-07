#!C:/Python/python.exe

# Set UTF-8 encoding for output
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-type:text/html; charset=utf-8\r\n\r\n")

import pymysql
import cgi, cgitb, os

cgitb.enable()
con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
cur = con.cursor()

q = """SELECT MAX(Id) FROM `adm_emp_addform`"""
cur.execute(q)
r = cur.fetchone()

if r[0] != None:
    n = r[0]
else:
    n = 0

z = ""
if n < 9:
    z = "000"
elif n >= 9 and n <= 99:
    z = "00"
elif n >= 100 and n < 999:
    z = "0"
else:
    z = ""

employeeid = "EMP" + z + str(n + 1)

print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Admin - Add Employee</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-dark-red: #cc0000;
            --asus-gray: #333333;
            --asus-light: #f5f5f5;
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;
            --sidebar-width: 250px;
            --sidebar-collapsed-width: 70px;
            --transition-speed: 0.3s;
            --form-glow: 0 0 15px rgba(255, 0, 0, 0.3);
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
            position: relative;
            color: #333;
        }

        /* Simplified background with subtle ASUS theme */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(245,245,245,0.9) 100%);
            z-index: -1;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        }

        .sidebar-header {
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(0, 0, 0, 0.8);
        }

        .sidebar-header img {
            width: 40px;
            margin-right: 10px;
        }

        .sidebar-header h3 {
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
        }

        .sidebar-header span {
            color: var(--asus-red);
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
            transition: all 0.3s ease;
        }

        .nav-link i {
            margin-right: 15px;
            font-size: 1.1rem;
            color: var(--asus-red);
        }

        .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
        }

        .nav-link.active {
            background: rgba(255, 0, 0, 0.2);
            border-left: 3px solid var(--asus-red);
        }

        .dropdown-menu {
            padding-left: 20px;
            display: none;
        }

        .dropdown-menu.show {
            display: block;
        }

        .logout {
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }

        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            width: calc(100% - var(--sidebar-width));
            padding: 30px;
            transition: all var(--transition-speed) ease;
            position: relative;
        }

        /* Form Container with Animations */
        .form-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
            animation: fadeInUp 0.8s ease;
            position: relative;
            overflow: hidden;
            border: 1px solid #eee;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .form-header {
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }

        .form-header h2 {
            color: var(--asus-gray);
            font-size: 1.8rem;
            margin-bottom: 10px;
            position: relative;
            display: inline-block;
        }

        .form-header h2::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background: var(--asus-red);
            border-radius: 3px;
            animation: underlineGrow 1s ease forwards;
        }

        @keyframes underlineGrow {
            from {
                width: 0;
            }
            to {
                width: 50px;
            }
        }

        /* Form Sections with Animation */
        .form-section {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
            animation: fadeIn 0.6s ease forwards;
        }

        .form-section-title {
            font-size: 1.2rem;
            color: var(--asus-gray);
            margin-bottom: 20px;
            position: relative;
            padding-left: 15px;
        }

        .form-section-title::before {
            content: '';
            position: absolute;
            left: 0;
            top: 5px;
            height: 60%;
            width: 4px;
            background: var(--asus-red);
            border-radius: 2px;
            animation: growHeight 0.8s ease forwards;
        }

        @keyframes growHeight {
            from {
                height: 0;
            }
            to {
                height: 60%;
            }
        }

        /* Form Elements */
        .form-row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -15px 20px;
        }

        .form-group {
            flex: 1 0 200px;
            padding: 0 15px;
            margin-bottom: 20px;
            position: relative;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--asus-gray);
            font-size: 0.9rem;
        }

        .form-control {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--asus-red);
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
        }

        /* Profile Picture Upload */
        .profile-picture-upload {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .profile-preview {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border: 2px solid #ddd;
            transition: all 0.3s ease;
        }

        .profile-preview:hover {
            transform: scale(1.05);
            border-color: var(--asus-red);
        }

        .profile-preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: none;
        }

        .profile-preview i {
            font-size: 2rem;
            color: #999;
        }

        /* Buttons with Animation */
        .form-actions {
            display: flex;
            justify-content: flex-end;
            margin-top: 30px;
            gap: 15px;
        }

        .btn {
            padding: 12px 25px;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            font-size: 0.9rem;
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background-color: var(--asus-red);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--asus-dark-red);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.2);
        }

        .btn-secondary {
            background-color: #f5f5f5;
            color: var(--asus-gray);
        }

        .btn-secondary:hover {
            background-color: #e0e0e0;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
            }
            .sidebar-header h3,
            .nav-link span {
                display: none;
            }
            .sidebar-header {
                justify-content: center;
                padding: 20px 0;
            }
            .nav-link {
                justify-content: center;
                padding: 15px 0;
            }
            .nav-link i {
                margin-right: 0;
                font-size: 1.3rem;
            }
            .main-content {
                margin-left: var(--sidebar-collapsed-width);
                padding: 15px;
            }
            .form-container {
                padding: 20px;
            }
            .form-group {
                flex: 1 0 100%;
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
        <div class="form-container">
            <div class="form-header">
                <h2>Employee Registration</h2>
                <p>Fill in the details to register a new employee</p>
            </div>

            <form id="employeeForm" action="" method="post" enctype="multipart/form-data">
                <div class="form-section">
                 

                    <div class="form-row">
                        <div class="form-group">
                            <label for="Name">Name</label>
                            <input type="text" id="Name" name="name" class="form-control" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" name="email" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="phone">Phone Number</label>
                            <input type="tel" id="phone" name="phone" class="form-control" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="dob">Date of Birth</label>
                            <input type="date" id="dob" name="dob" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="gender">Gender</label>
                            <select id="gender" name="gender" class="form-control form-select" required>
                                <option value="">Select Gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="address">Address</label>
                            <input type="text" id="address" name="address" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="city">City</label>
                            <input type="text" id="city" name="city" class="form-control" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="state">State</label>
                            <input type="text" id="state" name="state" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="pinCode">PIN Code</label>
                            <input type="text" id="pinCode" name="pinCode" class="form-control" required>
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="form-section-title">Employment Details</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="empid" class="form-label">Employee ID</label>
""")
print("""
                            <input type="text" class="form-control" id="employeeid" name="uemployeeid" value="%s" readonly required>
""" % employeeid)
print("""
                        </div>
                        <div class="form-group">
                            <label for="joinDate">Join Date</label>
                            <input type="date" id="joinDate" name="joinDate" class="form-control" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="department">Department</label>
                            <select id="department" name="department" class="form-control form-select" required>
                                <option value="">Select Department</option>
                                <option value="sales">Sales</option>
                                <option value="technical">Technical Support</option>
                                <option value="inventory">Inventory Management</option>
                                <option value="marketing">Marketing</option>
                                <option value="hr">Human Resources</option>
                               
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="position">Position</label>
                            <select id="position" name="position" class="form-control form-select" required>
                                <option value="">Select Position</option>
                                <option value="manager">Manager</option>
                                <option value=" Salesassistant">Sales Assistant</option>
                                <option value="technician">Technician</option>
                                <option value=" Sales executive">Sales Executive</option>
                                <option value=" Marketing specialist">Marketing</option>
                                <option value="HR">HR</option>
                                <option value="Inventory ">Inventory</option>
                                
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="salary">Salary</label>
                            <input type="number" id="salary" name="salary" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="shift">Shift</label>
                            <select id="shift" name="shift" class="form-control form-select" required>
                                <option value="">Select Shift</option>
                                <option value="morning">Morning (9AM-5PM)</option>
                                <option value="evening">Evening (1PM-9PM)</option>
                                <option value="full">Full Time</option>
                                <option value="part">Part Time</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="form-section-title">Account Information</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" class="form-control" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="confirmPassword">Confirm Password</label>
                            <input type="password" id="confirmPassword" name="confirmPassword" class="form-control" required>
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <button type="reset" class="btn btn-secondary">Reset</button>
                    <button type="submit" name="submit" class="btn btn-primary">Register Employee</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Profile picture preview
        document.getElementById('profilePicture').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const preview = document.getElementById('profilePreview');
                    const img = document.getElementById('profileImage');
                    const icon = preview.querySelector('i');

                    img.src = event.target.result;
                    img.style.display = 'block';
                    icon.style.display = 'none';
                };
                reader.readAsDataURL(file);
                document.getElementById('fileName').textContent = file.name;
                document.getElementById('fileName').style.display = 'block';
            }
        });

        // Form validation
        document.getElementById('employeeForm').addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
                return false;
            }
            return true;
        });
    </script>
</body>
</html>
""")

form = cgi.FieldStorage()

pname = form.getvalue("name")
pemailid = form.getvalue("email")
pphoneno = form.getvalue("phone")
pdob = form.getvalue("dob")
pgender = form.getvalue("gender")
paddress = form.getvalue("address")
pcity = form.getvalue("city")
pstate = form.getvalue("state")
ppincode = form.getvalue("pinCode")
pempid = form.getvalue("uemployeeid")
pjoinDate = form.getvalue("joinDate")
pdept = form.getvalue("department")
pposition = form.getvalue("position")
psalary = form.getvalue("salary")
pshift = form.getvalue("shift")
pusername = form.getvalue("username")
ppassword = form.getvalue("password")
pconfirmPassword = form.getvalue("confirmPassword")
psubmit = form.getvalue("submit")

if psubmit is not None:
    q2 = """INSERT INTO `adm_emp_addform` 
            (Name, Email_id, Phone, dob, gender, address, city, state, pincode, 
             EmpId, join_date, department, position, salary, shift, 
             user_name, password, confirm_password, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')"""
    cur.execute(q2, (pname, pemailid, pphoneno, pdob, pgender, paddress,
                     pcity, pstate, ppincode, pempid, pjoinDate, pdept,
                     pposition, psalary, pshift, pusername, ppassword, pconfirmPassword))
    con.commit()
    print("""
        <script>
            alert("Employee added successfully");
            window.location.href = "adm-emp-addform.py";
        </script>
    """)
    con.close()