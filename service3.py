#!C:/Python/python.exe
import smtplib
import sys
import io
import cgi
import cgitb
import pymysql

# Enable detailed error reporting
cgitb.enable(display=1, format="html")

# Set UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Process form submission first
form = cgi.FieldStorage()

# Print headers before any content
print("Content-type:text/html\r\n\r\n")

# Check if form was submitted
if 'submit' in form:
    try:
        # Get all form values
        pname = form.getvalue("uname", "").strip()
        pemailid = form.getvalue("email_id", "").strip()
        pphoneno = form.getvalue("phone", "").strip()
        paddress = form.getvalue("address", "").strip()
        pcity = form.getvalue("city", "").strip()
        ppincode = form.getvalue("pincode", "").strip()
        pservicetype = form.getvalue("serviceType", "").strip()
        pissue = form.getvalue("issueDescription", "").strip()

        # Validate required fields
        if not all([pname, pemailid, pphoneno, paddress, pcity, ppincode, pservicetype, pissue]):
            raise ValueError("All fields are required")

        # Database connection and insertion
        try:
            con = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="final_laptopproject",
                cursorclass=pymysql.cursors.DictCursor
            )

            with con:
                with con.cursor() as cur:
                    sql = """INSERT INTO service_form
                            (Name, Email_id, Phone, Address, City, Pin_code, Service_type, issue)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cur.execute(sql, (pname, pemailid, pphoneno, paddress, pcity, ppincode, pservicetype, pissue))
                con.commit()

            # Send confirmation email
            try:
                fromaddr = "s.nilesh4321@gmail.com"
                password = "nudohwfqpcevrojw"  # App password
                toaddr = pemailid
                subject = "ASUS Service Request Confirmation"
                body = f"""Dear {pname},

Thank you for submitting your service request to ASUS Showroom.

Service Request Details:
- Name: {pname}
- Email: {pemailid}
- Phone: {pphoneno}
- Service Type: {pservicetype}
- Issue Description: {pissue}

Our support team will contact you within 24 hours to discuss your service request.

Best regards,
ASUS Showroom Team
"""

                msg = f"Subject: {subject}\n\n{body}"

                server = smtplib.SMTP("smtp.gmail.com:587")
                server.ehlo()
                server.starttls()
                server.login(fromaddr, password)
                server.sendmail(fromaddr, toaddr, msg.encode('utf-8'))
                server.quit()

            except Exception as email_error:
                # If email fails, still show success but log the email error
                email_error_msg = f" (Note: Confirmation email failed to send: {str(email_error)})"
            else:
                email_error_msg = ""

            # Success response
            print("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Submission Successful</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
                <style>
                    .success-container {
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 30px;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    .success-icon {
                        color: #4CAF50;
                        font-size: 60px;
                        margin-bottom: 20px;
                    }
                    body {
                        background: linear-gradient(135deg, #000000, #1a1a2e);
                    }
                </style>
                <script>
                    setTimeout(function() {
                        window.location.href = "service3.py";
                    }, 5000);
                </script>
            </head>
            <body>
                <div class="container">
                    <div class="success-container animate__animated animate__fadeIn">
                        <div class="success-icon">
                            <span class="glyphicon glyphicon-ok"></span>
                        </div>
                        <h2>Service Request Submitted Successfully!</h2>
                        <p>Your service request has been received and a confirmation has been sent to your email address.</p>
                        <p>Our team will contact you within 24 hours.</p>
                        <p>You will be redirected back to the services page in 5 seconds.</p>
                        <a href="service3.py" class="btn btn-primary">Return Now</a>
                    </div>
                </div>
            </body>
            </html>
            """)
            sys.exit()

        except pymysql.Error as e:
            print(f"""
            <div class="container">
                <div class="alert alert-danger animate__animated animate__shakeX" style="margin-top: 50px;">
                    <h3>Database Error</h3>
                    <p>Error code: {e.args[0]}</p>
                    <p>Error message: {e.args[1]}</p>
                    <p>Please try again later or contact support.</p>
                    <a href="service3.py" class="btn btn-default">Back to Services</a>
                </div>
            </div>
            """)
            sys.exit()

    except Exception as e:
        print(f"""
        <div class="container">
            <div class="alert alert-danger animate__animated animate__shakeX" style="margin-top: 50px;">
                <h3>Error Processing Form</h3>
                <p>{str(e)}</p>
                <a href="service3.py" class="btn btn-default">Back to Services</a>
            </div>
        </div>
        """)
        sys.exit()

# Normal page display if no form submission
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Showroom - Services</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
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
            background: var(--asus-black);
            margin: 0;
            overflow-x: hidden;
            background-image: url('./img/asus-bg-pattern.png');
            background-attachment: fixed;
            background-size: cover;
        }

        /* Animated Header */
        .header {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(255, 0, 0, 0.3) 100%);
            padding: 40px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: headerGlow 8s infinite alternate;
        }

        @keyframes headerGlow {
            0% {
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
            }

            50% {
                box-shadow: 0 0 50px rgba(255, 0, 0, 0.6);
            }

            100% {
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
            }
        }

        .logo {
            height: 80px;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.7));
            animation: logoPulse 3s infinite;
        }

        @keyframes logoPulse {
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

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(to right, #fff, #ff0000);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
            animation: textGlow 2s infinite alternate;
        }

        @keyframes textGlow {
            from {
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            }

            to {
                text-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
            }
        }

        /* Enhanced Navbar */
        .navbar-inverse {
            background-color: rgba(0, 0, 0, 0.9);
            border: none;
            transition: all 0.5s;
        }

        .navbar-inverse.scrolled {
            background-color: rgba(0, 0, 0, 0.95);
            box-shadow: 0 5px 20px rgba(255, 0, 0, 0.3);
        }

        .navbar-inverse .navbar-nav>li>a {
            color: #fff;
            font-weight: 600;
            padding: 15px 20px;
            transition: all 0.3s;
            position: relative;
        }

        .navbar-inverse .navbar-nav>li>a:before {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: 0;
            left: 50%;
            background: var(--asus-red);
            transition: all 0.3s;
        }

        .navbar-inverse .navbar-nav>li>a:hover:before,
        .navbar-inverse .navbar-nav>li>a:focus:before {
            width: 80%;
            left: 10%;
        }

        .navbar-inverse .navbar-nav>.active>a {
            background-color: transparent;
            color: var(--asus-red);
        }

        .navbar-inverse .navbar-nav>.active>a:before {
            width: 80%;
            left: 10%;
        }

        /* Dropdown Menu Styling */
        .navbar-inverse .dropdown-menu {
            background-color: rgba(0, 0, 0, 0.95);
            border: 1px solid var(--asus-red);
        }

        .navbar-inverse .dropdown-menu>li>a {
            color: #fff;
            padding: 10px 20px;
            transition: all 0.3s;
        }

        .navbar-inverse .dropdown-menu>li>a:hover,
        .navbar-inverse .dropdown-menu>li>a:focus {
            background-color: var(--asus-red);
            color: #fff;
        }

        /* Service Hero Section */
        .service-hero {
            background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url('./img/service-bg.jpg');
            background-size: cover;
            background-attachment: fixed;
            color: white;
            padding: 100px 0;
            text-align: center;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }

        .service-hero:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path fill="rgba(255,0,0,0.05)" d="M0,0 L100,0 L100,100 L0,100 Z" /></svg>');
            background-size: 100px 100px;
            animation: gridAnimation 20s linear infinite;
        }

        @keyframes gridAnimation {
            0% { background-position: 0 0; }
            100% { background-position: 100px 100px; }
        }

        .service-hero h2 {
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            animation: fadeInDown 1s ease;
        }

        .service-hero p {
            font-size: 1.2rem;
            max-width: 700px;
            margin: 0 auto 30px;
            animation: fadeInUp 1s ease 0.3s both;
        }

        /* Service Cards */
        .service-card {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            height: 100%;
            border-top: 4px solid var(--asus-red);
            position: relative;
            overflow: hidden;
            color: white;
        }

        .service-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,0,0,0.1) 0%, rgba(255,0,0,0) 100%);
            z-index: 0;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }

        .service-card:hover:before {
            opacity: 1;
        }

        .service-card:hover .service-icon {
            transform: scale(1.2) rotate(10deg);
            color: var(--asus-red);
        }

        .service-icon {
            font-size: 50px;
            color: var(--asus-red);
            margin-bottom: 20px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        /* Service Form */
        .service-form {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
            border-top: 4px solid var(--asus-red);
            animation: fadeInRight 1s ease;
            color: white;
        }

        .service-form h3 {
            color: var(--asus-red);
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }

        .service-form h3:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 3px;
            background-color: var(--asus-red);
        }

        .form-control {
            height: 45px;
            border-radius: 4px;
            margin-bottom: 20px;
            border: 1px solid #444;
            transition: all 0.3s;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }

        .form-control:focus {
            border-color: var(--asus-red);
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        textarea.form-control {
            height: auto;
            min-height: 120px;
        }

        /* Custom dropdown styling */
        select.form-control {
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 10px center;
            background-size: 15px;
            padding-right: 30px;
        }

        /* Dropdown options styling */
        select.form-control option {
            background-color: #000;
            color: white;
        }

        /* Dropdown options hover effect */
        select.form-control option:hover {
            background-color: var(--asus-red) !important;
            color: white;
        }

        /* Firefox dropdown options styling */
        select.form-control option:checked {
            background-color: var(--asus-red);
            color: white;
        }

        /* Chrome/Safari dropdown options styling */
        select.form-control option:checked {
            background-color: var(--asus-red);
            color: white;
        }

        .btn-red {
            background-color: var(--asus-red);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            transition: all 0.3s;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        .btn-red:hover {
            background-color: #d40000;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
        }

        .btn-red:active {
            transform: translateY(0);
        }

        .btn-red:after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 5px;
            background: rgba(255, 255, 255, 0.5);
            opacity: 0;
            border-radius: 100%;
            transform: scale(1, 1) translate(-50%);
            transform-origin: 50% 50%;
        }

        .btn-red:focus:after {
            animation: ripple 1s ease-out;
        }

        @keyframes ripple {
            0% {
                transform: scale(0, 0);
                opacity: 1;
            }
            100% {
                transform: scale(20, 20);
                opacity: 0;
            }
        }

        .service-list {
            padding-left: 20px;
            color: white;
        }

        .service-list li {
            margin-bottom: 8px;
            position: relative;
            padding-left: 20px;
            color: white;
        }

        .service-list li:before {
            content: '•';
            color: var(--asus-red);
            font-size: 1.5em;
            position: absolute;
            left: 0;
            top: -3px;
        }

        .equal-height-row {
            display: flex;
            flex-wrap: wrap;
        }

        .equal-height-row>[class*='col-'] {
            display: flex;
        }

        /* Enhanced Footer */
        footer {
            padding: 60px 0 20px;
            background: linear-gradient(to right, #000, #1a1a1a, #000);
            color: #fff;
            position: relative;
            overflow: hidden;
        }

        footer:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--asus-red);
            animation: footerGlow 3s infinite;
        }

        @keyframes footerGlow {
            0% { box-shadow: 0 0 10px var(--asus-red); }
            50% { box-shadow: 0 0 20px var(--asus-red); }
            100% { box-shadow: 0 0 10px var(--asus-red); }
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .footer-section {
            margin-bottom: 30px;
            animation: fadeInUp 1s ease-out;
        }

        .footer-section h3 {
            color: var(--asus-red);
            font-size: 1.5rem;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }

        .footer-section h3:after {
            content: '';
            position: absolute;
            width: 50px;
            height: 2px;
            background: var(--asus-red);
            bottom: 0;
            left: 0;
        }

        .footer-section p,
        .footer-section a {
            color: #bbb;
            line-height: 1.8;
            transition: all 0.3s;
        }

        .footer-section a:hover {
            color: var(--asus-red);
            text-decoration: none;
            padding-left: 5px;
        }

        .social-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .social-links a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            color: #fff;
            transition: all 0.3s;
        }

        .social-links a:hover {
            background: var(--asus-red);
            transform: translateY(-5px);
        }

        .footer-bottom {
            text-align: center;
            padding-top: 40px;
            margin-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 1.5s ease-out;
        }

        .footer-bottom p {
            margin: 0;
            color: #888;
            font-size: 0.9rem;
        }

        /* Scroll to Top Button */
        .scroll-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: var(--asus-red);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: all 0.3s;
            z-index: 999;
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
        }

        .scroll-top.active {
            opacity: 1;
        }

        .scroll-top:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(255, 0, 0, 0.6);
        }

        /* Loading Animation for Form Submission */
        .loader {
            display: none;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 3px solid var(--asus-red);
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .service-hero {
                padding: 60px 0;
            }

            .service-hero h2 {
                font-size: 2rem;
            }

            .equal-height-row {
                display: block;
            }

            .equal-height-row>[class*='col-'] {
                display: block;
            }

            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Header with Animated Logo -->
    <header class="header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo" class="logo" />
        <h1>ASUS Premium Services</h1>
    </header>

    <!-- Enhanced Navbar -->
    <nav class="navbar navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#myNavbar">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div>

            <div class="collapse navbar-collapse" id="myNavbar">
                <ul class="nav navbar-nav">
                    <li><a href="./index.py">Home</a></li>
                    <li><a href="./about3.py">About</a></li>
                    <li class="active"><a href="./service3.py">Service</a></li>
                    <li><a href="./models.py">Laptops</a></li>
                    <li><a href="./contact1.py">Contact</a></li>
                </ul>
               <ul class="nav navbar-nav navbar-right">
                    <li><a href="./register.py"><span class="glyphicon glyphicon-calendar"></span> Register & Booking </a></li>

                    </li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <i class="fas fa-user"></i> Account <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="./admin_login.py"><i class="fas fa-sign-in-alt"></i> Admin</a></li>
                            <li><a href="./employee_login.py"><i class="fas fa-sign-in-alt"></i> Employee</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="service-hero">
        <div class="container">
            <h2 class="animate__animated animate__fadeInDown">Premium Services for Your ASUS Devices</h2>
            <p class="animate__animated animate__fadeInUp">Expert care and support for all your ASUS products</p>
        </div>
    </div>

    <div class="container">
        <div class="row equal-height-row">
            <div class="col-md-8">
                <div class="row equal-height-row">
                    <div class="col-md-6">
                        <div class="service-card animate__animated animate__fadeInLeft">
                            <div class="service-icon">
                                <span class="glyphicon glyphicon-wrench"></span>
                            </div>
                            <h3 style="text-align: center;">Hardware Repairs</h3>
                            <p>Professional repair services for screens, keyboards, motherboards, and other hardware
                                components using genuine ASUS parts.</p>
                            <ul class="service-list">
                                <li>Screen replacement</li>
                                <li>Battery replacement</li>
                                <li>Motherboard repair</li>
                                <li>Keyboard repair</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="service-card animate__animated animate__fadeInRight">
                            <div class="service-icon">
                                <span class="glyphicon glyphicon-hdd"></span>
                            </div>
                            <h3 style="text-align: center;">Software Support</h3>
                            <p>Comprehensive software solutions including OS installation, driver updates, and virus
                                removal.</p>
                            <ul class="service-list">
                                <li>Windows installation</li>
                                <li>Driver updates</li>
                                <li>Virus removal</li>
                                <li>Data backup</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="service-card animate__animated animate__fadeInLeft animate__delay-1s">
                            <div class="service-icon">
                                <span class="glyphicon glyphicon-certificate"></span>
                            </div>
                            <h3 style="text-align: center;">Warranty Services</h3>
                            <p>Claim your warranty benefits with our authorized service center for ASUS products.</p>
                            <ul class="service-list">
                                <li>Warranty registration</li>
                                <li>Warranty claims</li>
                                <li>Extended warranty</li>
                                <li>International warranty</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="service-card animate__animated animate__fadeInRight animate__delay-1s">
                            <div class="service-icon">
                                <span class="glyphicon glyphicon-headphones"></span>
                            </div>
                            <h3 style="text-align: center;">Premium Support</h3>
                            <p>24/7 dedicated support for your ASUS devices with priority service.</p>
                            <ul class="service-list">
                                <li>Priority service queue</li>
                                <li>On-site technical support</li>
                                <li>Remote desktop assistance</li>
                                <li>Dedicated support hotline</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="service-form">
                    <h3>Request Service</h3>
                    <p>Fill out the form below and our team will contact you within 24 hours</p>
                    <form id="service" name="profile" method="post" enctype="multipart/form-data" onsubmit="document.getElementById('loader').style.display='block';">
                        <div class="form-group">
                            <input type="text" class="form-control" id="fullname" name="uname" placeholder="Your Name"
                                required>
                        </div>
                        <div class="form-group">
                            <input type="email" class="form-control" id="email" name="email_id"
                                placeholder="Email Address" required>
                        </div>
                        <div class="form-group">
                            <input type="tel" class="form-control" id="phone" name="phone" placeholder="Phone Number"
                                required>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="address" name="address"
                                placeholder="Full Address" required>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="city" name="city" placeholder="City" required>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="pincode" name="pincode" placeholder="PIN Code"
                                required>
                        </div>
                        <div class="form-group">
                            <label for="serviceType">Service Type</label>
                            <select id="serviceType" name="serviceType" class="form-control" required>
                                <option value="">Select Service Type</option>
                                <option value="hardware">Hardware Repair</option>
                                <option value="software">Software Support</option>
                                <option value="warranty">Warranty Service</option>
                                <option value="premium">Premium Support</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <textarea id="issueDescription" name="issueDescription" class="form-control" rows="5"
                                placeholder="Describe your issue" required></textarea>
                        </div>
                        <button type="submit" name="submit" class="btn btn-red">
                            <span id="submit-text">Submit Request</span>
                            <div id="loader" class="loader" style="display: none;"></div>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h3>About ASUS</h3>
                <p>ASUS is a worldwide top-three consumer notebook vendor and maker of the world's best-selling, most
                    award-winning motherboards.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-facebook-f"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-youtube"></i></a>
                </div>
            </div>

            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="./index.py">Home</a></li>
                    <li><a href="./models.py">Products</a></li>
                    <li><a href="./service3.py">Services</a></li>
                    <li><a href="./about3.py">About Us</a></li>
                    <li><a href="./contact1.py">Contact</a></li>
                </ul>
            </div>

            <div class="footer-section">
                <h3>Contact Info</h3>
                <p><i class="fas fa-map-marker-alt"></i> 123 Tech Plaza, Bangalore, India</p>
                <p><i class="fas fa-phone"></i> +91 80 1234 5678</p>
                <p><i class="fas fa-envelope"></i> info@asus-showroom.com</p>
                <p><i class="fas fa-clock"></i> Mon-Sat: 10:00 AM - 8:00 PM</p>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; 2025 ASUS Premium Showroom. All Rights Reserved. | Designed with <i class="fas fa-heart"
                    style="color: var(--asus-red);"></i> by Your Team</p>
        </div>
    </footer>

    <!-- Scroll to Top Button -->
    <div class="scroll-top">
        <i class="fas fa-arrow-up"></i>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

    <script>
        // Navbar scroll effect
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.navbar-inverse').addClass('scrolled');
            } else {
                $('.navbar-inverse').removeClass('scrolled');
            }
        });

        // Scroll to top button
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
                $('.scroll-top').addClass('active');
            } else {
                $('.scroll-top').removeClass('active');
            }
        });

        $('.scroll-top').click(function () {
            $('html, body').animate({ scrollTop: 0 }, 'slow');
            return false;
        });

        // Smooth scrolling for all links
        $("a").on('click', function (event) {
            if (this.hash !== "") {
                event.preventDefault();
                var hash = this.hash;
                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800, function () {
                    window.location.hash = hash;
                });
            }
        });

        // Add animation to elements when they come into view
        $(document).ready(function() {
            // Animate service cards on scroll
            $(window).scroll(function() {
                $('.service-card').each(function() {
                    var cardPosition = $(this).offset().top;
                    var scrollPosition = $(window).scrollTop() + $(window).height();

                    if (scrollPosition > cardPosition) {
                        $(this).addClass('animate__animated animate__fadeInUp');
                    }
                });
            });

            // Form submission loader
            $('form').submit(function() {
                $('#submit-text').hide();
                $('#loader').show();
            });

            // Add hover effect to all service cards
            $('.service-card').hover(
                function() {
                    $(this).addClass('animate__animated animate__pulse');
                },
                function() {
                    $(this).removeClass('animate__animated animate__pulse');
                }
            );
        });
    </script>
</body>
</html>
""")