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
    <title>ASUS Premium Showroom</title>
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

        /* Caret color for dropdown */
        .navbar-inverse .navbar-nav .dropdown-toggle .caret {
            border-top-color: #fff;
            border-bottom-color: #fff;
        }

        .navbar-inverse .navbar-nav .open .dropdown-toggle .caret {
            border-top-color: var(--asus-red);
            border-bottom-color: var(--asus-red);
        }

        /* Animated Carousel */
        .carousel-inner .item {
            transition: transform 1s ease, opacity .5s ease;
        }

        .carousel-caption {
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            bottom: 100px;
            animation: captionSlide 1s ease-out;
        }

        @keyframes captionSlide {
            from {
                transform: translateY(50px);
                opacity: 0;
            }

            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        /* Laptop Showcase Section */
        .asus-showroom {
            padding: 80px 0;
            background: rgba(0, 0, 0, 0.8);
            position: relative;
            overflow: hidden;
        }

        .asus-showroom:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('./img/asus-circuit-pattern.png') center/cover;
            opacity: 0.1;
            z-index: -1;
        }

        .asus-showroom h1 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            background: linear-gradient(to right, #fff, #ff0000);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: textGlow 2s infinite alternate;
        }

        .asus-showroom h2 {
            font-size: 2.5rem;
            margin-bottom: 40px;
            color: #fff;
            position: relative;
            display: inline-block;
        }

        .asus-showroom h2:after {
            content: '';
            position: absolute;
            width: 50%;
            height: 3px;
            background: var(--asus-red);
            bottom: -10px;
            left: 25%;
            animation: lineExpand 1.5s ease-out;
        }

        @keyframes lineExpand {
            from {
                width: 0;
                left: 50%;
            }

            to {
                width: 50%;
                left: 25%;
            }
        }

        /* Enhanced Explore Button */
        .explore-btn {
            display: inline-block;
            margin: 30px 0;
            padding: 15px 40px;
            background: linear-gradient(45deg, var(--asus-red), #d40000);
            color: white;
            font-size: 1.2rem;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.4s;
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
            text-decoration: none;
        }

        .explore-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.6);
            text-decoration: none;
            color: white;
        }

        .explore-btn:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .explore-btn:hover:before {
            left: 100%;
        }

        /* Laptop Grid Animation */
        .laptop-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 0 20px;
            margin-top: 50px;
        }

        .laptop-card {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.5s;
            border: 1px solid rgba(255, 0, 0, 0.3);
            overflow: hidden;
            position: relative;
            animation: fadeInUp 1s ease-out;
            animation-fill-mode: both;
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

        .laptop-card:nth-child(1) {
            animation-delay: 0.2s;
        }

        .laptop-card:nth-child(2) {
            animation-delay: 0.4s;
        }

        .laptop-card:nth-child(3) {
            animation-delay: 0.6s;
        }

        .laptop-card:nth-child(4) {
            animation-delay: 0.8s;
        }

        .laptop-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(255, 0, 0, 0.3);
            border-color: var(--asus-red);
        }

        .laptop-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255, 0, 0, 0.05), transparent);
            z-index: -1;
        }

        .laptop-card img {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 20px;
            transition: all 0.5s;
            filter: brightness(0.9);
        }

        .laptop-card:hover img {
            transform: scale(1.03);
            filter: brightness(1);
        }

        .laptop-card h3 {
            font-size: 1.5rem;
            color: #fff;
            margin-bottom: 15px;
            position: relative;
            display: inline-block;
        }

        .laptop-card h3:after {
            content: '';
            position: absolute;
            width: 30%;
            height: 2px;
            background: var(--asus-red);
            bottom: -5px;
            left: 0;
            transition: all 0.3s;
        }

        .laptop-card:hover h3:after {
            width: 100%;
        }

        .laptop-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .laptop-card ul li {
            padding: 8px 0;
            color: #ccc;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
            position: relative;
            padding-left: 25px;
        }

        .laptop-card ul li:before {
            content: '▹';
            position: absolute;
            left: 0;
            color: var(--asus-red);
        }
        .laptop-card {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.laptop-card .btn-container {
    margin-top: auto;
    padding-top: 20px;
    text-align: center;
}

        /* Intro Section */
        .intro {
            padding: 80px 20px;
            text-align: center;
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), url('./img/asus-tech-bg.jpg') center/cover;
            position: relative;
            overflow: hidden;
        }

        .intro h2 {
            font-size: 2.8rem;
            margin-bottom: 30px;
            color: #fff;
            position: relative;
            display: inline-block;
            animation: fadeIn 1s ease-out;
        }

        .intro p {
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.8;
            color: #ddd;
            animation: fadeIn 1.5s ease-out;
        }

        /* New Featured Categories Section */
        .categories-section {
            padding: 80px 0;
            background: rgba(10, 10, 10, 0.9);
        }

        .category-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .category-tab {
            padding: 15px 30px;
            margin: 0 10px;
            background: transparent;
            color: #aaa;
            border: none;
            border-bottom: 3px solid transparent;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .category-tab.active,
        .category-tab:hover {
            color: white;
            border-bottom: 3px solid var(--asus-red);
        }

        .category-content {
            display: none;
        }

        .category-content.active {
            display: block;
            animation: fadeIn 0.5s ease-out;
        }

        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 30px;
            padding: 0 20px;
        }

        .category-item {
            background: rgba(30, 30, 30, 0.7);
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .category-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .category-item img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }

        .category-info {
            padding: 20px;
        }

        .category-info h4 {
            margin: 0 0 10px;
            color: white;
        }

        .category-info p {
            color: #aaa;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .category-link {
            color: var(--asus-red);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
        }

        .category-link i {
            margin-left: 5px;
            transition: transform 0.3s;
        }

        .category-link:hover {
            color: white;
        }

        .category-link:hover i {
            transform: translateX(5px);
        }

        /* Promo Banner Section */
        .promo-banner {
            background: linear-gradient(90deg, #000000, #1a1a1a, #000000);
            padding: 60px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            margin: 40px 0;
        }

        .promo-banner:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('./img/asus-circuit-lines.png') center/cover;
            opacity: 0.1;
            z-index: 0;
        }

        .promo-content {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
        }

        .promo-banner h2 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: white;
        }

        .promo-banner p {
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto 30px;
            color: #ddd;
        }

        .promo-timer {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }

        .timer-box {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid var(--asus-red);
            border-radius: 5px;
            padding: 15px 20px;
            min-width: 80px;
        }

        .timer-value {
            font-size: 2rem;
            font-weight: 700;
            color: white;
        }

        .timer-label {
            font-size: 0.8rem;
            color: #aaa;
            text-transform: uppercase;
        }

        /* Why Choose ASUS Section */
        .features-section {
            padding: 80px 0;
            background: rgba(0, 0, 0, 0.7);
        }

        .features-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            margin-top: 50px;
        }

        .feature-card {
            text-align: center;
            padding: 30px;
            background: rgba(30, 30, 30, 0.5);
            border-radius: 10px;
            transition: all 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(255, 0, 0, 0.2);
            border-color: var(--asus-red);
        }

        .feature-icon {
            font-size: 3rem;
            color: var(--asus-red);
            margin-bottom: 20px;
        }

        .feature-card h3 {
            color: white;
            margin-bottom: 15px;
        }

        .feature-card p {
            color: #aaa;
            line-height: 1.6;
        }

        /* Testimonials Section */
        .testimonials-section {
            padding: 80px 0;
            background: url('./img/asus-testimonial-bg.jpg') center/cover;
            position: relative;
        }

        .testimonials-section:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
        }

        .testimonials-container {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .testimonial-slider {
            margin-top: 50px;
        }

        .testimonial-item {
            background: rgba(30, 30, 30, 0.8);
            padding: 30px;
            border-radius: 10px;
            margin: 0 15px;
            border-left: 3px solid var(--asus-red);
        }

        .testimonial-text {
            color: #ddd;
            font-style: italic;
            margin-bottom: 20px;
            position: relative;
        }

        .testimonial-text:before {
            content: '"';
            font-size: 4rem;
            color: rgba(255, 0, 0, 0.2);
            position: absolute;
            top: -20px;
            left: -15px;
            font-family: serif;
        }

        .testimonial-author {
            display: flex;
            align-items: center;
        }

        .author-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 15px;
            border: 2px solid var(--asus-red);
        }

        .author-info h4 {
            margin: 0;
            color: white;
        }

        .author-info p {
            margin: 5px 0 0;
            color: #aaa;
            font-size: 0.9rem;
        }

        .testimonial-rating {
            color: gold;
            margin-top: 5px;
        }

        /* Enhanced Footer */
        footer {
            background: linear-gradient(to right, #000, #1a1a1a, #000);
            color: #fff;
            padding: 60px 0 20px;
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
            0% {
                box-shadow: 0 0 10px var(--asus-red);
            }

            50% {
                box-shadow: 0 0 20px var(--asus-red);
            }

            100% {
                box-shadow: 0 0 10px var(--asus-red);
            }
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
            color: var(white);
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
            color: white;
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

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .asus-showroom h1 {
                font-size: 2.5rem;
            }

            .asus-showroom h2 {
                font-size: 2rem;
            }

            .intro h2 {
                font-size: 2rem;
            }

            .laptop-grid {
                grid-template-columns: 1fr;
            }

            .category-tabs {
                flex-direction: column;
                align-items: center;
            }

            .category-tab {
                margin: 5px 0;
                width: 100%;
                text-align: center;
            }

            .promo-banner h2 {
                font-size: 2rem;
            }

            .promo-timer {
                flex-wrap: wrap;
            }
        }

        /* Animation Classes */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }

        .animated {
            animation-duration: 1s;
            animation-fill-mode: both;
        }

        /* New Newsletter Section */
        .newsletter-section {
            padding: 60px 20px;
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(255, 0, 0, 0.2));
            text-align: center;
        }

        .newsletter-container {
            max-width: 800px;
            margin: 0 auto;
        }

        .newsletter-form {
            display: flex;
            max-width: 600px;
            margin: 30px auto 0;
        }

        .newsletter-input {
            flex: 1;
            padding: 15px 20px;
            border: none;
            border-radius: 50px 0 0 50px;
            font-size: 1rem;
            background: rgba(255, 255, 255, 0.9);
        }

        .newsletter-btn {
            padding: 15px 30px;
            background: var(--asus-red);
            color: white;
            border: none;
            border-radius: 0 50px 50px 0;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .newsletter-btn:hover {
            background: #d40000;
        }

        .newsletter-text {
            margin-top: 20px;
            color: #aaa;
            font-size: 0.9rem;
        }
    </style>
</head>

<body>
    <!-- Header with Animated Logo -->
    <header class="header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo" class="logo" />
        <h1>Welcome To ASUS Premium Showroom</h1>
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
                    <li class="active"><a href="./index.py">Home</a></li>
                    <li><a href="./about3.py">About</a></li>
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

    <!-- Animated Carousel -->
    <div id="myCarousel" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
            <li data-target="#myCarousel" data-slide-to="1"></li>
            <li data-target="#myCarousel" data-slide-to="2"></li>
        </ol>

        <div class="carousel-inner">
            <div class="item active">
                <img src="./img/ROG Strix g17.jpg" alt="ROG Strix" style="width:100%; height:600px; object-fit: cover;">
                <div class="carousel-caption">
                    <h3>ROG Strix Series</h3>
                    <p>Ultimate gaming performance with cutting-edge technology</p>
                    <a href="./models.py" class="explore-btn">Explore Now</a>
                </div>
            </div>
            <div class="item">
                <img src="./img/strix-g15-2022.png" alt="Strix G15"
                    style="width:100%; height:600px; object-fit: cover;">
                <div class="carousel-caption">
                    <h3>Strix G15</h3>
                    <p>Power meets portability in our flagship gaming laptop</p>
                    <a href="./models.py" class="explore-btn">Shop Now</a>
                </div>
            </div>
            <div class="item">
                <img src="./img/wallpaper .jpg" alt="ASUS Wallpaper"
                    style="width:100%; height:600px; object-fit: cover;">
                <div class="carousel-caption">
                    <h3>Innovation Redefined</h3>
                    <p>Discover the future of computing with ASUS</p>
                    <a href="./models.py" class="explore-btn">View Collection</a>
                </div>
            </div>
        </div>

        <a class="left carousel-control" href="#myCarousel" data-slide="prev">
            <span class="glyphicon glyphicon-chevron-left"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="right carousel-control" href="#myCarousel" data-slide="next">
            <span class="glyphicon glyphicon-chevron-right"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>

   <!-- Laptop Showcase Section -->
<section class="asus-showroom">
    <div class="text-center">
        <h2>Explore the Latest ASUS 2025 Laptop Models</h2>
        <p class="lead" style="color: #aaa; max-width: 800px; margin: 0 auto;">Discover our award-winning laptops
            with cutting-edge technology and innovative designs</p>
    </div>

    <div class="laptop-grid">
        <!-- Zenbook A14 -->
        <div class="laptop-card">
            <img src="./img/zenbook a14.jpg" alt="ASUS Zenbook A14">
            <h3>Zenbook A14</h3>
            <ul>
                <li>🌟 Ultra-lightweight (under 1kg)</li>
                <li>🔋 70Wh battery, Snapdragon X chipset</li>
                <li>🖥️ 14" Lumina OLED display</li>
                <li>🧠 Copilot+ AI features</li>
            </ul>
            <div class="text-center" style="margin-top: auto; padding-top: 20px;">
                <a href="./models.py" class="explore-btn" style="padding: 10px 25px; font-size: 1rem; display: inline-block;">View Details</a>
            </div>
        </div>

        <!-- ROG Strix SCAR 18 -->
        <div class="laptop-card">
            <img src="./img/ROG Strix g17.jpg" alt="ROG Strix SCAR 17">
            <h3>ROG Strix SCAR 18</h3>
            <ul>
                <li>🎮 Intel Core Ultra 9 / AMD Ryzen 9</li>
                <li>💾 Up to 64GB DDR5 RAM</li>
                <li>📦 Up to 4TB PCIe Gen 4 SSD</li>
                <li>💡 AniMe Matrix™ display</li>
            </ul>
            <div class="text-center" style="margin-top: auto; padding-top: 20px;">
                <a href="./models.py" class="explore-btn" style="padding: 10px 25px; font-size: 1rem; display: inline-block;">View Details</a>
            </div>
        </div>

        <!-- TUF Gaming A18 -->
        <div class="laptop-card">
            <img src="./img/asus tuf a15.jpg" alt="TUF Gaming A15">
            <h3>TUF Gaming A18</h3>
            <ul>
                <li>🧱 AMD Ryzen 7 260, RTX 5070 GPU</li>
                <li>🖥️ 16" 2.5K 165Hz display</li>
                <li>🛡️ Military-grade durability</li>
                <li>🧊 Advanced cooling system</li>
            </ul>
            <div class="text-center" style="margin-top: auto; padding-top: 20px;">
                <a href="./models.py" class="explore-btn" style="padding: 10px 25px; font-size: 1rem; display: inline-block;">View Details</a>
            </div>
        </div>

        <!-- Zenbook DUO -->
        <div class="laptop-card">
            <img src="./img/zen book duo.webp" alt="ASUS Zenbook DUO">
            <h3>Zenbook DUO</h3>
            <ul>
                <li>🖥️ Dual 14" 3K OLED touchscreens</li>
                <li>🧠 Intel Core Ultra 9 processor</li>
                <li>⌨️ Detachable ErgoSense keyboard</li>
                <li>🔋 75Wh battery for all-day use</li>
            </ul>
            <div class="text-center" style="margin-top: auto; padding-top: 20px;">
                <a href="./models.py" class="explore-btn" style="padding: 10px 25px; font-size: 1rem; display: inline-block;">View Details</a>
            </div>
        </div>
    </div>

    <div class="text-center" style="margin-top: 50px;">
        <a href="./models.py" class="explore-btn">View All Laptops</a>
    </div>
</section>





   <!-- Why Choose ASUS Section -->
<section class="features-section">
    <div class="features-container">
        <div class="text-center">
            <h2 style="color: white; margin-bottom: 20px;">Why Choose ASUS?</h2>
            <p style="color: #aaa; max-width: 800px; margin: 0 auto;">Discover what makes ASUS laptops stand out from the competition with our industry-leading innovations</p>
        </div>

        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-award"></i>
                </div>
                <h3>Award-Winning Design</h3>
                <p>Our laptops consistently win prestigious design awards for their innovative form factors and premium build quality, recognized by iF Design, Red Dot, and CES Innovation awards.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-microchip"></i>
                </div>
                <h3>Cutting-Edge Technology</h3>
                <p>We incorporate the latest processors, graphics, and display technologies before they become mainstream, including OLED displays, AI-enhanced chipsets, and liquid metal cooling.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3>Military-Grade Durability</h3>
                <p>Many of our laptops undergo rigorous MIL-STD-810H testing to ensure they can withstand extreme temperatures, humidity, vibration, and accidental drops.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-headset"></i>
                </div>
                <h3>Premium Support</h3>
                <p>Enjoy peace of mind with our comprehensive warranty and dedicated customer support team available 24/7, plus exclusive services like 1-year accidental damage protection.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-palette"></i>
                </div>
                <h3>Stunning Visuals</h3>
                <p>Experience industry-leading displays with our ASUS Lumina OLED technology, offering 100% DCI-P3 color gamut, Pantone validation, and ultra-low blue light emissions.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-leaf"></i>
                </div>
                <h3>Eco-Friendly Innovation</h3>
                <p>We're committed to sustainability with eco-friendly packaging, reduced carbon footprint, and ENERGY STAR® certified products that meet strict energy efficiency guidelines.</p>
            </div>
        </div>
    </div>
</section>
    <!-- Testimonials Section -->
    <section class="testimonials-section">
        <div class="testimonials-container">
            <div class="text-center">
                <h2 style="color: white; margin-bottom: 20px;">What Our Customers Say</h2>
                <p style="color: #aaa; max-width: 800px; margin: 0 auto;">Hear from satisfied ASUS laptop owners around
                    the world</p>
            </div>

            <div class="testimonial-slider">
                <div id="testimonialCarousel" class="carousel slide" data-ride="carousel">
                    <ol class="carousel-indicators">
                        <li data-target="#testimonialCarousel" data-slide-to="0" class="active"></li>
                        <li data-target="#testimonialCarousel" data-slide-to="1"></li>
                        <li data-target="#testimonialCarousel" data-slide-to="2"></li>
                    </ol>

                    <div class="carousel-inner">
                        <div class="item active">
                            <div class="testimonial-item">
                                <div class="testimonial-text">
                                    My ROG Strix G18 is an absolute beast! The performance is incredible for both gaming
                                    and content creation. The cooling system keeps everything running smoothly even
                                    during marathon sessions.
                                </div>
                                <div class="testimonial-author">
                                    <img src="./img/1000038538.jpg" alt="Customer" class="author-avatar">
                                    <div class="author-info">
                                        <h4>nilesh</h4>
                                        <p>Professional Gamer</p>
                                        <div class="testimonial-rating">
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="item">
                            <div class="testimonial-item">
                                <div class="testimonial-text">
                                    As a graphic designer, the ProArt StudioBook has transformed my workflow. The
                                    color-accurate display and powerful specs handle all my Adobe apps with ease. It's
                                    worth every penny!
                                </div>
                                <div class="testimonial-author">
                                    <img src="./img/images (2).jpg" alt="Customer" class="author-avatar">
                                    <div class="author-info">
                                        <h4>Priya</h4>
                                        <p>Graphic Designer</p>
                                        <div class="testimonial-rating">
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                            <i class="fas fa-star"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="item">
                            <div class="testimonial-item">
                                <div class="testimonial-text">
                                    The Zenbook DUO's second screen is a game-changer for productivity. I can have my
                                    email on the second screen while working on documents. Battery life is impressive
                                    too!
                                </div>
                                <div class="testimonial-author">
                                    <img src="./img/images3.png" alt="Customer" class="author-avatar">
                                    <div class="author-info">
                                        <h4>Arjun</h4>
                                        <p>Business Consultant</p>
                                        <div class="testimonial-rating">
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
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Newsletter Section -->
    <section class="newsletter-section">
        <div class="newsletter-container">
            <h2 style="color: white;">Stay Updated</h2>
            <p style="color: #aaa; max-width: 600px; margin: 10px auto;">Register to our newsletter for the latest
                product releases, exclusive offers, and tech news.</p>



        </div>
    </section>

    <!-- Intro Section -->
    <section class="intro">
        <h2>Explore the Power of Innovation</h2>
        <p>Step into the world of ASUS laptops—where performance meets design. From the ultra-sleek ZenBook series and
            powerful ROG gaming rigs to versatile Vivobooks and business-ready ExpertBooks, our showroom offers the
            latest in cutting-edge technology to elevate every experience. Discover the perfect blend of power,
            portability, and style that fits your lifestyle.</p>
        
    </section>

    <!-- Enhanced Footer -->
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
                <h3>Support</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="#">Warranty Information</a></li>
                    <li><a href="#">Product Registration</a></li>
                    <li><a href="#">Driver Downloads</a></li>
                    <li><a href="#">FAQ</a></li>
                    <li><a href="#">Contact Support</a></li>
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

        // Carousel animation
        $('.carousel').carousel({
            interval: 5000,
            pause: "hover"
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

        // Category tabs functionality
        $('.category-tab').click(function () {
            $('.category-tab').removeClass('active');
            $(this).addClass('active');

            var tabId = $(this).data('tab') + '-category';
            $('.category-content').removeClass('active');
            $('#' + tabId).addClass('active');
        });

        // Countdown timer for promo banner
        function updateCountdown() {
            const endDate = new Date();
            endDate.setDate(endDate.getDate() + 7); // 7 days from now

            const now = new Date().getTime();
            const distance = endDate - now;

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            $('#days').text(days.toString().padStart(2, '0'));
            $('#hours').text(hours.toString().padStart(2, '0'));
            $('#minutes').text(minutes.toString().padStart(2, '0'));
            $('#seconds').text(seconds.toString().padStart(2, '0'));
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);

        // Newsletter form submission
        $('.newsletter-form').submit(function (e) {
            e.preventDefault();
            alert('Thank you for subscribing to our newsletter!');
            $(this).trigger('reset');
        });
    </script>
</body>

</html>
""")