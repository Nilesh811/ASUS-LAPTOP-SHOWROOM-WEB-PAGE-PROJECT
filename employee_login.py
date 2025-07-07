#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql

# Enable debugging and set UTF-8 output
cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Print content-type header FIRST
print("Content-type:text/html\r\n\r\n")

# Database connection and form processing
try:
    form = cgi.FieldStorage()
    username = form.getvalue("username")
    password = form.getvalue("password")
    psubmit = form.getvalue("submit")

    if psubmit is not None:
        con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
        cur = con.cursor()

        # Use parameterized query to prevent SQL injection
        q = "SELECT id FROM `adm_emp_addform` WHERE Empid=%s AND password=%s"
        cur.execute(q, (username, password))
        res = cur.fetchone()

        if res is not None:
            print(f"""
            <script>
            alert("Login is successful");
            window.location.href="emp1-dash.py?id={res[0]}";
            </script>""")
            sys.exit()  # Exit after successful login
        else:
            print("""<script>
            alert("Invalid username or password");
            </script>""")

except pymysql.Error as e:
    print(f"<script>alert('Database error: {str(e)}');</script>")
except Exception as e:
    print(f"<script>alert('Error: {str(e)}');</script>")
finally:
    if 'con' in locals() and con.open:
        con.close()

# HTML content
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Premium Showroom - Employee Login</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --asus-red: #ff0000;
            --asus-black: #000000;
            --asus-gray: #1a1a1a;
            --text-light: #f8f9fa;
        }

        body {
            font-family: 'Montserrat', sans-serif;
            color: var(--text-light);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            background: url('./img/wallpaperflare.com_wallpaper (4).jpg') no-repeat center center fixed;
            background-size: cover;
            position: relative;
        }

        body:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: -1;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        .login-box {
            background: rgba(0, 0, 0, 0.85);
            border-radius: 15px;
            width: 400px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            border: 1px solid var(--asus-red);
            position: relative;
            overflow: hidden;
            transform: scale(0.9);
            transition: all 0.5s ease;
            animation: slideUp 0.8s ease-out forwards;
        }

        @keyframes slideUp {
            from {
                transform: translateY(50px) scale(0.9);
                opacity: 0;
            }

            to {
                transform: translateY(0) scale(1);
                opacity: 1;
            }
        }

        .login-box:hover {
            box-shadow: 0 20px 45px rgba(255, 0, 0, 0.3);
        }

        .login-box:before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(to bottom right,
                    transparent 0%,
                    rgba(255, 0, 0, 0.1) 50%,
                    transparent 100%);
            transform: rotate(30deg);
            animation: shine 3s infinite;
        }

        @keyframes shine {
            0% {
                transform: rotate(30deg) translate(-30%, -30%);
            }

            100% {
                transform: rotate(30deg) translate(30%, 30%);
            }
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo img {
            height: 60px;
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.7));
            animation: pulse 2s infinite;
        }

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

        .login-title {
            text-align: center;
            margin-bottom: 30px;
            color: white;
            font-weight: 700;
            font-size: 24px;
            position: relative;
        }

        .login-title:after {
            content: '';
            position: absolute;
            width: 50px;
            height: 3px;
            background: var(--asus-red);
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
        }

        .form-group {
            margin-bottom: 25px;
            position: relative;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #ddd;
            font-weight: 600;
        }

        .form-control {
            width: 100%;
            padding: 12px 15px;
            background: rgba(30, 30, 30, 0.8);
            border: 1px solid #333;
            border-radius: 5px;
            color: white;
            transition: all 0.3s;
        }

        .form-control:focus {
            border-color: var(--asus-red);
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
            outline: none;
        }

        .input-icon {
            position: absolute;
            right: 15px;
            top: 38px;
            color: #777;
        }

        .back-btn {
            width: 100%;
            padding: 12px;
            background: rgba(30, 30, 30, 0.8);
            border: 1px solid #333;
            border-radius: 5px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
            position: relative;
            overflow: hidden;
        }

        .back-btn:hover {
            background: rgba(50, 50, 50, 0.8);
            border-color: var(--asus-red);
            color: var(--asus-red);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .back-btn:active {
            transform: translateY(0);
        }

        .back-btn i {
            margin-right: 8px;
        }

        .login-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(to right, #d40000, var(--asus-red));
            border: none;
            border-radius: 5px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
        }

        .login-btn:hover {
            background: linear-gradient(to right, var(--asus-red), #ff3333);
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 0, 0, 0.3);
        }

        .login-btn:active {
            transform: translateY(0);
        }

        .login-btn:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .login-btn:hover:before {
            left: 100%;
        }

        .forgot-password {
            text-align: right;
            margin-top: 10px;
        }

        .forgot-password a {
            color: #aaa;
            text-decoration: none;
            font-size: 13px;
            transition: all 0.3s;
        }

        .forgot-password a:hover {
            color: var(--asus-red);
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 15px 25px;
            border-radius: 5px;
            border-left: 4px solid var(--asus-red);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            transform: translateX(150%);
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 1000;
            max-width: 300px;
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification i {
            margin-right: 10px;
            color: var(--asus-red);
        }

        @media (max-width: 480px) {
            .login-box {
                width: 90%;
                padding: 30px 20px;
            }
        }
    </style>
</head>

<body>
    <div class="login-container">
        <div class="login-box">
            <div class="logo">
                <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            </div>
            <h2 class="login-title">EMPLOYEE DASHBOARD LOGIN</h2>

            <form id="loginForm" method="POST" action="employee_login.py">
                <div class="form-group">
                    <label for="username">Employee ID</label>
                    <input type="text" class="form-control" id="username" name="username" placeholder="Enter your employee ID" required>
                    <i class="fas fa-user input-icon"></i>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password" required>
                    <i class="fas fa-lock input-icon"></i>
                </div>

                <div class="forgot-password">
                    <a href="#">Forgot Password?</a>
                </div>
                <button type="submit" name="submit" value="Login" class="login-btn">LOGIN</button>
                <br> <br>
                <button type="button" class="back-btn" id="backButton">
                    <i class="fas fa-arrow-left"></i> BACK
                </button>
            </form>
        </div>
    </div>

    <div class="notification" id="notification">
        <i class="fas fa-info-circle"></i>
        <span id="notification-message">Welcome to ASUS Employee Dashboard</span>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script>
        $(document).ready(function () {
            // Back button functionality
            $('#backButton').click(function () {
                window.location.href = 'index.py';
            });

            // Notification function
            function showNotification(message, type = 'info') {
                const notification = $('#notification');
                const notificationMsg = $('#notification-message');

                // Set message and style based on type
                notificationMsg.text(message);

                // Remove all previous classes
                notification.removeClass('info error success');

                // Add appropriate class
                notification.addClass(type);

                // Change icon based on type
                const icon = notification.find('i');
                switch (type) {
                    case 'error':
                        icon.removeClass().addClass('fas fa-exclamation-circle');
                        notification.css('border-left-color', '#ff3333');
                        break;
                    case 'success':
                        icon.removeClass().addClass('fas fa-check-circle');
                        notification.css('border-left-color', '#00cc66');
                        break;
                    default:
                        icon.removeClass().addClass('fas fa-info-circle');
                        notification.css('border-left-color', 'var(--asus-red)');
                }

                // Show notification
                notification.addClass('show');

                // Hide after 5 seconds
                setTimeout(function () {
                    notification.removeClass('show');
                }, 5000);
            }

            // Initial notification
            setTimeout(function () {
                showNotification('Welcome to ASUS Employee Dashboard Login');
            }, 1000);

            // Prevent form resubmission on page refresh
            if (window.history.replaceState) {
                window.history.replaceState(null, null, window.location.href);
            }
        });
    </script>
</body>
</html>
""")