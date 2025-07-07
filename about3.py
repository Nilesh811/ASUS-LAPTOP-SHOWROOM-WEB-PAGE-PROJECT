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
    <title>About ASUS Laptop Showroom</title>
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
        /* About page specific styles */
        .hero-header {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('./img/showroom-bg.jpg') center/cover no-repeat;
            color: var(--text-light);
            padding: 120px 0;
            text-align: center;
            position: relative;
        }

        .btn-asus {
            background-color: var(--asus-red);
            color: white;
            padding: 12px 30px;
            border-radius: 4px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
        }

        .btn-asus:hover {
            background-color: #d40000;
            color: white;
            transform: translateY(-2px);
        }

        .section-title {
            color: white;
            position: relative;
            padding-bottom: 15px;
            margin-bottom: 30px;
            text-align: center;
        }

        .section-title:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 3px;
            background: var(--asus-red);
        }

        .about-feature-box {
            padding: 30px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 30px;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            background: rgba(30, 30, 30, 0.8);
            color: #ddd;
            border: 1px solid rgba(255, 0, 0, 0.3);
        }

        .about-feature-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .feature-icon {
            font-size: 50px;
            color: var(--asus-red);
            margin-bottom: 20px;
        }

        .timeline {
            position: relative;
            padding: 40px 0;
        }

        .timeline-item {
            position: relative;
            padding-left: 80px;
            margin-bottom: 50px;
            color: #ddd;
        }

        .timeline-date {
            position: absolute;
            left: 0;
            top: 0;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--asus-red);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .team-card {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            transition: all 0.3s;
            border: 1px solid rgba(255, 0, 0, 0.3);
            color: #ddd;
        }

        .team-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .team-img {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }

        .testimonial-card {
            background: rgba(30, 30, 30, 0.8);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            border: 1px solid rgba(255, 0, 0, 0.3);
            color: #ddd;
        }

        .testimonial-card:hover {
            box-shadow: 0 15px 30px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .testimonial-img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin: 0 auto 20px;
            border: 3px solid var(--asus-red);
        }

        .stats-box {
            text-align: center;
            padding: 30px 15px;
            background: rgba(30, 30, 30, 0.8);
            color: white;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 0, 0, 0.3);
        }

        .stats-box:hover {
            box-shadow: 0 15px 30px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .stats-number {
            font-size: 42px;
            font-weight: 700;
            color: var(--asus-red);
            margin: 15px 0;
        }

        /* Content sections */
        .content-section {
            padding: 80px 0;
            background: rgba(0, 0, 0, 0.7);
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
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
        <h1>About ASUS Premium Showroom</h1>
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
                    <li class="active"><a href="./about3.py">About</a></li>
                    <li><a href="./service3.py">Service</a></li>
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

    <!-- Hero Header -->
    <section class="hero-header">
        <div class="container">
            <h2>Your trusted destination for premium laptops and exceptional service</h2>
        </div>
    </section>

    <!-- About Section -->
<section class="content-section" style="background-color: rgba(0, 0, 0, 0.7);">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <h2 class="section-title">Our Story</h2>
                <p style="color: white; font-weight: bold;">
                    Founded in 2010, our Laptop Showroom has grown from a small retail outlet to become one of the
                    most trusted authorized dealers in the region. Our journey began with a simple mission: to
                    bring cutting-edge technology to customers with exceptional service.
                </p>
                <p style="color: white; font-weight: bold;">
                    Over the years, we've helped thousands of customers find their perfect laptop, from students
                    needing affordable options to professional gamers demanding peak performance. Our knowledgeable
                    staff and commitment to after-sales support have made us a favorite among tech enthusiasts.
                </p>
            </div>
            <div class="col-md-6">
                <img src="./img/asus showroom interior.jpg" alt="Showroom Interior" class="img-responsive"
                    style="border-radius: 8px; width: 100%;">
            </div>
        </div>
    </div>
</section>

    <!-- Features Section -->
    <section class="content-section" style="background-color: rgba(0, 0, 0, 0.8);">
        <div class="container">
            <h2 class="section-title">Why Choose Us</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="about-feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-award"></i>
                        </div>
                        <h3>Authorized Dealer</h3>
                        <p>We offer genuine products with full manufacturer warranties and support.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="about-feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-laptop"></i>
                        </div>
                        <h3>Hands-On Experience</h3>
                        <p>Test any model in our showroom before you buy to ensure it meets your needs.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="about-feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-headset"></i>
                        </div>
                        <h3>Expert Support</h3>
                        <p>Our certified technicians provide setup assistance and after-sales service.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="content-section">
        <div class="container">
            <div class="row">
                <div class="col-md-3 col-sm-6">
                    <div class="stats-box">
                        <i class="fas fa-laptop" style="font-size: 30px; color: var(--asus-red);"></i>
                        <div class="stats-number">500+</div>
                        <p>Laptop Models</p>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="stats-box">
                        <i class="fas fa-users" style="font-size: 30px; color: var(--asus-red);"></i>
                        <div class="stats-number">10,000+</div>
                        <p>Satisfied Customers</p>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="stats-box">
                        <i class="fas fa-certificate" style="font-size: 30px; color: var(--asus-red);"></i>
                        <div class="stats-number">15</div>
                        <p>Certified Technicians</p>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="stats-box">
                        <i class="fas fa-trophy" style="font-size: 30px; color: var(--asus-red);"></i>
                        <div class="stats-number">8</div>
                        <p>Industry Awards</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Team Section -->
    <section class="content-section" style="background-color: rgba(0, 0, 0, 0.8);">
        <div class="container">
            <h2 class="section-title">Meet Our Team</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="team-card">
                        <img src="./img/Team Member1.jpg" alt="Team Member" class="team-img">
                        <div class="p-3">
                            <h3>Rajesh Kumar</h3>
                            <p class="text-muted">Showroom Manager</p>
                            <p>15+ years experience in computer retail and product specialist.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="team-card">
                        <img src="./img/Team Member2.jpg" alt="Team Member" class="team-img">
                        <div class="p-3">
                            <h3>Priya Sharma</h3>
                            <p class="text-muted">Sales Director</p>
                            <p>Helps customers find their perfect laptop with expert advice.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="team-card">
                        <img src="./img/Team Member3.jpg" alt="Team Member" class="team-img">
                        <div class="p-3">
                            <h3>Sanjay Patel</h3>
                            <p class="text-muted">Technical Lead</p>
                            <p>Certified technician with expertise in hardware repairs.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials -->
    <section class="content-section">
        <div class="container">
            <h2 class="section-title">What Our Customers Say</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="testimonial-card text-center">
                        <h3>Amit Singh</h3>
                        <div class="text-muted mb-3">Professional Gamer</div>
                        <p>"The team helped me configure the perfect gaming laptop. Their product knowledge is
                            unmatched!"</p>
                        <div style="color: var(--asus-red);">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="testimonial-card text-center">
                        <h3>Neha Gupta</h3>
                        <div class="text-muted mb-3">Graphic Designer</div>
                        <p>"My laptop works flawlessly for design work. The staff helped me choose the perfect specs."
                        </p>
                        <div style="color: var(--asus-red);">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="testimonial-card text-center">
                        <h3>Arjun Mehta</h3>
                        <div class="text-muted mb-3">Business Owner</div>
                        <p>"We've purchased 20+ laptops from this showroom. Their corporate discounts and service are
                            excellent."</p>
                        <div style="color: var(--asus-red);">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star-half-alt"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

  

    <!-- Footer -->
    <footer style="background: linear-gradient(to right, #000, #1a1a1a, #000); color: #fff; padding: 60px 0 20px; position: relative; overflow: hidden;">
        <div class="footer-content" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; max-width: 1200px; margin: 0 auto; padding: 0 20px;">
            <div class="footer-section">
                <h3 style="color: var(--asus-red); font-size: 1.5rem; margin-bottom: 20px; position: relative; padding-bottom: 10px;">About ASUS</h3>
                <p style="color: #bbb; line-height: 1.8;">ASUS is a worldwide top-three consumer notebook vendor and maker of the world's best-selling, most award-winning motherboards.</p>
                <div class="social-links" style="display: flex; gap: 15px; margin-top: 20px;">
                    <a href="#" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; color: #fff; transition: all 0.3s;"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; color: #fff; transition: all 0.3s;"><i class="fab fa-twitter"></i></a>
                    <a href="#" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; color: #fff; transition: all 0.3s;"><i class="fab fa-instagram"></i></a>
                    <a href="#" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; color: #fff; transition: all 0.3s;"><i class="fab fa-youtube"></i></a>
                </div>
            </div>

            <div class="footer-section">
                <h3 style="color: var(--asus-red); font-size: 1.5rem; margin-bottom: 20px; position: relative; padding-bottom: 10px;">Quick Links</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="./index.py" style="color: #bbb; line-height: 1.8; transition: all 0.3s;">Home</a></li>
                    <li><a href="./models.py" style="color: #bbb; line-height: 1.8; transition: all 0.3s;">Products</a></li>
                    <li><a href="./service3.py" style="color: #bbb; line-height: 1.8; transition: all 0.3s;">Services</a></li>
                    <li><a href="./about3.py" style="color: #bbb; line-height: 1.8; transition: all 0.3s;">About Us</a></li>
                    <li><a href="./contact1.py" style="color: #bbb; line-height: 1.8; transition: all 0.3s;">Contact</a></li>
                </ul>
            </div>

            <div class="footer-section">
                <h3 style="color: var(--asus-red); font-size: 1.5rem; margin-bottom: 20px; position: relative; padding-bottom: 10px;">Contact Info</h3>
                <p style="color: #bbb; line-height: 1.8;"><i class="fas fa-map-marker-alt"></i> 123 Tech Plaza, Bangalore, India</p>
                <p style="color: #bbb; line-height: 1.8;"><i class="fas fa-phone"></i> +91 80 1234 5678</p>
                <p style="color: #bbb; line-height: 1.8;"><i class="fas fa-envelope"></i> info@asus-showroom.com</p>
                <p style="color: #bbb; line-height: 1.8;"><i class="fas fa-clock"></i> Mon-Sat: 10:00 AM - 8:00 PM</p>
            </div>
        </div>

        <div class="footer-bottom" style="text-align: center; padding-top: 40px; margin-top: 40px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="margin: 0; color: #888; font-size: 0.9rem;">&copy; 2025 ASUS Premium Showroom. All Rights Reserved. | Designed with <i class="fas fa-heart" style="color: var(--asus-red);"></i> by Your Team</p>
        </div>
    </footer>

    <!-- Scroll to Top Button -->
    <div class="scroll-top" style="position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px; background: var(--asus-red); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; opacity: 0; transition: all 0.3s; z-index: 999; box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);">
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
    </script>
</body>

</html>
""")