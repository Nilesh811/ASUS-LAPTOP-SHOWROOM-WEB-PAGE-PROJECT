#!C:/Python/python.exe
import sys
import io
import cgi
import cgitb
import pymysql

# Enable debugging
cgitb.enable()

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-type:text/html\r\n\r\n")
print("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact ASUS Showroom</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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
        /* Contact Page Specific Styles with Black Background */
        body {
            font-family: 'Segoe UI', sans-serif;
            color: #fff;
            background-color: var(--asus-black);
            background-image: url('./img/asus-bg-pattern.png');
            background-attachment: fixed;
            background-size: cover;
        }

        .contact-section {
            padding: 60px 30px;
            background: rgba(0, 0, 0, 0.7);
        }

        .contact-section h2 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 40px;
            color: var(--asus-white);
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
        }

        .contact-container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .contact-info {
            flex: 1 1 450px;
            background: rgba(30, 30, 30, 0.9);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 0, 0, 0.3);
        }

        .contact-info h3 {
            margin-bottom: 20px;
            color: #fff;
            border-bottom: 2px solid var(--asus-red);
            padding-bottom: 10px;
        }

        .contact-details {
            margin-bottom: 25px;
        }

        .contact-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        .contact-icon {
            color: var(--asus-red);
            font-size: 1.2rem;
            margin-right: 15px;
            margin-top: 3px;
            min-width: 20px;
        }

        .contact-text h4 {
            margin: 0 0 5px 0;
            color: #fff;
            font-size: 1.1rem;
        }

        .contact-text p,
        .contact-text a {
            margin: 0;
            color: #ccc;
            text-decoration: none;
            transition: color 0.3s;
        }

        .contact-text a:hover {
            color: var(--asus-red);
        }

        .showroom-hours {
            margin-top: 30px;
        }

        .hours-table {
            width: 100%;
            border-collapse: collapse;
            color: #ccc;
        }

        .hours-table tr:nth-child(even) {
            background-color: rgba(50, 50, 50, 0.5);
        }

        .hours-table td {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .hours-table td:first-child {
            font-weight: 600;
            color: #fff;
        }

        .showroom-features {
            margin-top: 30px;
        }

        .features-list {
            list-style-type: none;
            padding: 0;
            color: #ccc;
        }

        .features-list li {
            padding: 8px 0;
            display: flex;
            align-items: center;
        }

        .features-list li::before {
            content: "✓";
            color: var(--asus-red);
            font-weight: bold;
            margin-right: 10px;
        }

        .contact-map {
            flex: 1 1 450px;
            min-height: 400px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 0, 0, 0.3);
        }

        .back-button {
            display: inline-block;
            margin-top: 40px;
            padding: 12px 30px;
            background-color: var(--asus-red);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            border: none;
        }

        .back-button:hover {
            background-color: #fff;
            color: var(--asus-red);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(255, 0, 0, 0.4);
        }

        .button-container {
            text-align: center;
            width: 100%;
            margin-top: 30px;
        }

        /* Footer Styles from models.py */
        footer {
            background: linear-gradient(to right, #000000, #1a1a1a, #000000);
            color: white;
            padding: 40px 0 20px;
            font-family: 'Montserrat', sans-serif;
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .footer-section h3 {
            font-size: 1.3em;
            margin-bottom: 20px;
            color: var(--asus-red);
            position: relative;
            display: inline-block;
        }

        .footer-section h3::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 50px;
            height: 2px;
            background: var(--asus-red);
        }

        .footer-section p, .footer-section ul {
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.6;
        }

        .footer-section ul {
            list-style: none;
            padding: 0;
        }

        .footer-section ul li {
            margin-bottom: 10px;
        }

        .footer-section ul li a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer-section ul li a:hover {
            color: var(--asus-red);
        }

        .social-links {
            margin-top: 20px;
        }

        .social-links a {
            display: inline-block;
            width: 35px;
            height: 35px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            text-align: center;
            line-height: 35px;
            margin-right: 10px;
            color: white;
            transition: all 0.3s;
        }

        .social-links a:hover {
            background: var(--asus-red);
            transform: translateY(-3px);
        }

        .footer-bottom {
            text-align: center;
            padding-top: 20px;
            margin-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .footer-content {
                grid-template-columns: 1fr;
            }
            
            .contact-container {
                flex-direction: column;
            }
            
            .contact-info, .contact-map {
                flex: 1 1 100%;
            }
        }
    </style>
</head>

<body>
    <!-- Header with Animated Logo from models.py -->
    <header class="header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo" class="logo" />
        <h1>ASUS Premium Showroom</h1>
    </header>

    <!-- Enhanced Navbar from models.py -->
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
                    <li><a href="./service3.py">Service</a></li>
                    <li><a href="./models.py">Laptops</a></li>
                    <li class="active"><a href="./contact1.py">Contact</a></li>
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

    <!-- Contact Page Content with Black Background -->
    <section class="contact-section">
        <h2>ASUS Showroom Contact Details</h2>
        <div class="contact-container">
            <div class="contact-info">
                <h3>ASUS Official Showroom</h3>

                <div class="contact-details">
                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-map-marker-alt"></i>
                        </div>
                        <div class="contact-text">
                            <h4>Showroom Address</h4>
                            <p>ASUS Exclusive Store, Tech Plaza, 123 Innovation Road, Bengaluru, Karnataka 560001, India
                            </p>
                        </div>
                    </div>

                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-phone-alt"></i>
                        </div>
                        <div class="contact-text">
                            <h4>Phone Numbers</h4>
                            <p>Sales: <a href="tel:+918012345678">+91 80 1234 5678</a></p>
                            <p>Support: <a href="tel:+918098765432">+91 80 9876 5432</a></p>
                        </div>
                    </div>

                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-envelope"></i>
                        </div>
                        <div class="contact-text">
                            <h4>Email Addresses</h4>
                            <p>Sales: <a href="mailto:sales@asus-showroom.in">sales@asus-showroom.in</a></p>
                            <p>Support: <a href="mailto:support@asus-showroom.in">support@asus-showroom.in</a></p>
                        </div>
                    </div>
                </div>

                <div class="showroom-hours">
                    <h4>Showroom Hours</h4>
                    <table class="hours-table">
                        <tr>
                            <td>Monday - Friday</td>
                            <td>10:00 AM - 8:00 PM</td>
                        </tr>
                        <tr>
                            <td>Saturday</td>
                            <td>10:00 AM - 9:00 PM</td>
                        </tr>
                        <tr>
                            <td>Sunday</td>
                            <td>11:00 AM - 7:00 PM</td>
                        </tr>
                        <tr>
                            <td>Public Holidays</td>
                            <td>11:00 AM - 6:00 PM</td>
                        </tr>
                    </table>
                </div>

                <div class="showroom-features">
                    <h4>Showroom Features</h4>
                    <ul class="features-list">
                        <li>Experience Zone with latest ASUS laptops and devices</li>
                        <li>Expert product demonstrations</li>
                        <li>On-site technical support</li>
                        <li>Exclusive showroom-only deals</li>
                        <li>Gaming laptop testing station</li>
                        <li>Creator series workstation demo</li>
                        <li>Student and corporate discounts available</li>
                    </ul>
                </div>
            </div>

            <div class="contact-map">
                <iframe
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1002538.0383642152!2d75.79938287812502!3d11.026303400000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba85708b7f632d5%3A0xd85b2bbff1ecebb3!2sIIE%20HOPES%20-%20Data%20Analytics%20%7C%20Mernstack%20%7C%20Python%20%7C%20Tally%20Training%20institute!5e0!3m2!1sen!2sin!4v1745481253060!5m2!1sen!2sin"
                    width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
        </div>
       
    </section>

    <!-- Footer from models.py -->
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

    <!-- jQuery and Bootstrap JS -->
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
    </script>
</body>

</html>
      """)