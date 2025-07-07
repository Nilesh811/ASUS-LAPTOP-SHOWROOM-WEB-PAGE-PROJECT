#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Enable debugging
cgitb.enable()

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Print HTML header
print("Content-type:text/html\r\n\r\n")

# Get form data
form = cgi.FieldStorage()

# Process form submission if submitted
if 'submit' in form:
    # Get form values
    pname = form.getvalue("name")
    pemailid = form.getvalue("email")
    pphoneno = form.getvalue("phone")
    paddress = form.getvalue("address")
    pcity = form.getvalue("city")
    ppincode = form.getvalue("pincode")
    pdate = form.getvalue("date")

    # Database connection and insertion
    try:
        con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
        cur = con.cursor()

        q2 = """INSERT INTO register (Name, Email_id, Phone, Address, City, Pin_code, Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(q2, (pname, pemailid, pphoneno, paddress, pcity, ppincode, pdate))
        con.commit()

        # Email sending configuration
        fromaddr = "s.nilesh4321@gmail.com"
        password = "nudohwfqpcevrojw"
        toaddr = pemailid
        subject = "Welcome to ASUS Premium Laptop Showroom"

        # Create email body
        body = f"""Dear {pname},

Thank you for registering with ASUS Premium Laptop Showroom!

Your registration details:
- Name: {pname}
- Email: {pemailid}
- Phone: {pphoneno}
- Visit Date: {pdate}

We're excited to welcome you to our showroom on {pdate}. Our team will contact you shortly to confirm your visit.

At ASUS, we're committed to providing you with the best gaming and productivity laptop experience. Our showroom features the latest ROG (Republic of Gamers) and ZenBook series.

If you have any questions before your visit, please don't hesitate to contact us.

Best regards,
ASUS Showroom Team
"""

        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = fromaddr
        message['To'] = toaddr
        message['Subject'] = subject

        # Attach body to the email
        message.attach(MIMEText(body, 'plain'))

        try:
            # Create SMTP session
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Enable security
            server.login(fromaddr, password)  # Login with credentials
            text = message.as_string()
            server.sendmail(fromaddr, toaddr, text)  # Send email
            server.quit()  # Terminate session

            # Show success message
            print("""
            <script>
                alert("Registration successful! Confirmation email sent.");
                window.location.href = "bookinglap.py";
            </script>
            """)
        except smtplib.SMTPException as e:
            print(f"""
            <script>
                alert("Registration successful but email could not be sent: {str(e)}");
                window.location.href = "bookinglap.py";
            </script>
            """)

    except pymysql.Error as e:
        print(f"<h3>Database Error: {e}</h3>")
    finally:
        if 'con' in locals() and con:
            con.close()

# Rest of your HTML content remains the same...

# HTML content
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom Registration</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --asus-red: #FF0000;
            --asus-black: #000000;
            --asus-gray: #333333;
            --asus-light: #F5F5F5;
        }

        body {
            margin: 0;
            padding: 0;
            background: url('./img/wallpaperflare.com_wallpaper (4).jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden;
        }

        .main-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
        }

        .form-container {
            width: 450px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            border: 1px solid var(--asus-red);
            transform-style: preserve-3d;
            perspective: 1000px;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotateY(0deg);
            }
            50% {
                transform: translateY(-20px) rotateY(5deg);
            }
        }

        .form-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(to bottom right,
                    transparent,
                    transparent,
                    transparent,
                    var(--asus-red));
            transform: rotate(30deg);
            animation: shine 3s infinite;
            opacity: 0.3;
        }

        @keyframes shine {
            0% {
                left: -50%;
            }
            100% {
                left: 150%;
            }
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
            animation: fadeIn 1s ease-out;
        }

        .logo img {
            width: 150px;
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.5));
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

        .title {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: 1px;
            position: relative;
        }

        .title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background: var(--asus-red);
            border-radius: 3px;
        }

        .input-group {
            position: relative;
            margin-bottom: 25px;
            animation: slideIn 0.5s ease-out forwards;
            opacity: 0;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .input-group:nth-child(1) {
            animation-delay: 0.1s;
        }

        .input-group:nth-child(2) {
            animation-delay: 0.2s;
        }

        .input-group:nth-child(3) {
            animation-delay: 0.3s;
        }

        .input-group:nth-child(4) {
            animation-delay: 0.4s;
        }

        .input-group:nth-child(5) {
            animation-delay: 0.5s;
        }

        .input-group:nth-child(6) {
            animation-delay: 0.6s;
        }

        .input-group:nth-child(7) {
            animation-delay: 0.7s;
        }

        .input-group:nth-child(8) {
            animation-delay: 0.8s;
        }

        .input-group input,
        .input-group select {
            width: 100%;
            padding: 15px 45px 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: white;
            font-size: 16px;
            transition: all 0.3s;
            backdrop-filter: blur(5px);
            box-sizing: border-box;
        }

        .input-group input:focus,
        .input-group select:focus {
            outline: none;
            border-color: var(--asus-red);
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        }

        .input-group label {
            position: absolute;
            top: 15px;
            left: 20px;
            color: #aaa;
            pointer-events: none;
            transition: all 0.3s;
            background: transparent;
            padding: 0 5px;
        }

        .input-group input:focus + label,
        .input-group input:not(:placeholder-shown) + label,
        .input-group select:valid + label {
            top: -10px;
            left: 15px;
            font-size: 12px;
            background: var(--asus-black);
            color: var(--asus-red);
            border-radius: 5px;
            padding: 0 8px;
        }

        .input-group i {
            position: absolute;
            right: 20px;
            top: 15px;
            color: #aaa;
            pointer-events: none;
        }

        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, var(--asus-red), #d40000);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7);
            }
            70% {
                box-shadow: 0 0 0 15px rgba(255, 0, 0, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
            }
        }

        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 0, 0, 0.3);
        }

        .submit-btn::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .submit-btn:hover::after {
            left: 100%;
        }

        .login-link {
            text-align: center;
            color: #aaa;
            animation: fadeIn 1s ease-out 0.7s forwards;
            opacity: 0;
        }

        .login-link a {
            color: var(--asus-red);
            text-decoration: none;
            transition: all 0.3s;
        }

        .login-link a:hover {
            text-decoration: underline;
        }

        .confirmation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 100;
            opacity: 0;
            pointer-events: none;
            transition: all 0.5s;
        }

        .confirmation.active {
            opacity: 1;
            pointer-events: all;
        }

        .confirmation img {
            width: 150px;
            margin-bottom: 30px;
            transform: scale(0.5);
            transition: all 0.5s;
        }

        .confirmation.active img {
            transform: scale(1);
        }

        .confirmation h2 {
            color: white;
            font-size: 32px;
            margin-bottom: 20px;
            transform: translateY(30px);
            opacity: 0;
            transition: all 0.5s;
        }

        .confirmation.active h2 {
            transform: translateY(0);
            opacity: 1;
        }

        .confirmation p {
            color: #aaa;
            font-size: 18px;
            margin-bottom: 30px;
            max-width: 500px;
            text-align: center;
            line-height: 1.6;
            transform: translateY(30px);
            opacity: 0;
            transition: all 0.5s 0.2s;
        }

        .confirmation.active p {
            transform: translateY(0);
            opacity: 1;
        }

        .redirect-btn {
            padding: 12px 30px;
            background: var(--asus-red);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            transform: scale(0);
            transition: all 0.5s 0.4s;
        }

        .confirmation.active .redirect-btn {
            transform: scale(1);
        }

        .redirect-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        }

        /* Add placeholder styling */
        .input-group input::placeholder {
            color: transparent;
        }

        /* Date input specific styling */
        input[type="date"]::-webkit-calendar-picker-indicator {
            filter: invert(0.7);
            cursor: pointer;
        }

        input[type="date"]::-webkit-calendar-picker-indicator:hover {
            filter: invert(1);
        }
    </style>
</head>

<body>
    <div class="main-container">
        <div class="form-container">
            <div class="logo">
                <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
            </div>

            <h2 class="title">ASUS SHOWROOM REGISTRATION</h2>

            <form id="registrationForm" name="profile" method="post" enctype="multipart/form-data">
                <div class="input-group">
                    <input type="text" id="name" name="name" required placeholder=" ">
                    <label for="name">Name</label>
                    <i class="fas fa-user"></i>
                </div>

                <div class="input-group">
                    <input type="email" id="email" name="email" required placeholder=" ">
                    <label for="email">Email Address</label>
                    <i class="fas fa-envelope"></i>
                </div>

                <div class="input-group">
                    <input type="tel" id="phone" name="phone" required placeholder=" ">
                    <label for="phone">Phone Number</label>
                    <i class="fas fa-phone"></i>
                </div>

                <div class="input-group">
                    <input type="text" id="address" name="address" required placeholder=" ">
                    <label for="address">Full Address</label>
                    <i class="fas fa-map-marker-alt"></i>
                </div>

                <div class="input-group">
                    <input type="text" id="city" name="city" required placeholder=" ">
                    <label for="city">City</label>
                    <i class="fas fa-globe-asia"></i>
                </div>

                <div class="input-group">
                    <input type="text" id="pincode" name="pincode" required placeholder=" ">
                    <label for="pincode">PIN Code</label>
                    <i class="fas fa-map-pin"></i>
                </div>

                <div class="input-group">
                    <input type="text" id="date" name="date" onfocus="(this.type='date')" required placeholder=" ">
                    <label for="date">Preferred Visit Date</label>
                    <i class="fas fa-calendar"></i>
                </div>

                <button type="submit" name="submit" class="submit-btn">REGISTER NOW</button>

                <div class="login-link">
                    Already registered? <a href="#">Login here</a>
                </div>
            </form>
        </div>
    </div>

    <div class="confirmation" id="confirmation">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
        <h2>Thank You for Registering!</h2>
        <p>Your registration has been successfully submitted. Our ASUS representative will contact you shortly to confirm your showroom visit details.</p>
        <button class="redirect-btn" id="redirectBtn">Continue to ASUS Homepage</button>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const form = document.getElementById('registrationForm');
            const confirmation = document.getElementById('confirmation');
            const redirectBtn = document.getElementById('redirectBtn');

            form.addEventListener('submit', function (e) {
                // Show confirmation animation
                confirmation.classList.add('active');

                // Prevent default form submission (we'll let the server handle it)
                // e.preventDefault();

                // Here you would typically send the form data to a server
                // For demo, we'll just log it
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    address: document.getElementById('address').value,
                    city: document.getElementById('city').value,
                    pincode: document.getElementById('pincode').value,
                    date: document.getElementById('date').value
                };

                console.log('Form submitted:', formData);
            });

            redirectBtn.addEventListener('click', function () {
                // Redirect to bookinglap.py
                window.location.href = 'bookinglap.py';
            });

            // Add animation to input fields on focus
            const inputs = document.querySelectorAll('.input-group input');
            inputs.forEach(input => {
                input.addEventListener('focus', function () {
                    this.parentElement.style.transform = 'scale(1.02)';
                    this.parentElement.style.zIndex = '10';
                });

                input.addEventListener('blur', function () {
                    this.parentElement.style.transform = 'scale(1)';
                    this.parentElement.style.zIndex = '1';
                });
            });

            // Initialize labels based on existing values
            inputs.forEach(input => {
                if (input.value) {
                    input.dispatchEvent(new Event('blur'));
                }
            });
        });
    </script>
</body>

</html>
""")