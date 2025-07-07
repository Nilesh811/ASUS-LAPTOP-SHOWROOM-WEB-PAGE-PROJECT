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
    <title>ASUS 2025 Laptop Models</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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

        .asus-showroom {
            padding: 80px 30px 60px;
            background: linear-gradient(to bottom, #000000, #1a1a1a);
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
            color: white;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Category Tabs */
        .category-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .category-tab {
            padding: 12px 25px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            border: 1px solid var(--asus-red);
            color: white;
            margin: 5px;
        }

        .category-tab:hover {
            background: rgba(255, 0, 0, 0.3);
            transform: translateY(-3px);
        }

        .category-tab.active {
            background: var(--asus-red);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
        }

        .category-section {
            display: none;
            animation: fadeIn 0.5s ease-in-out;
        }

        .category-section.active {
            display: block;
        }

        .section-title {
            text-align: left;
            margin: 20px 30px 30px;
            color: var(--asus-red);
            font-size: 1.8em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            padding-bottom: 10px;
        }

        .section-title:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 3px;
            background: var(--asus-red);
        }

        /* Laptop Grid */
        .laptop-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 0 20px;
            margin-bottom: 40px;
        }

        /* Enhanced Laptop Card */
        .laptop-card {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            transition: all 0.4s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            overflow: hidden;
            position: relative;
            backdrop-filter: blur(5px);
            transform-style: preserve-3d;
            perspective: 1000px;
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .laptop-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0) 50%);
            z-index: -1;
            transition: all 0.5s ease;
            opacity: 0;
        }

        .laptop-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 35px rgba(255, 0, 0, 0.3);
            border-color: var(--asus-red);
            background: rgba(40, 40, 40, 0.9);
        }

        .laptop-card:hover::before {
            opacity: 1;
        }

        .laptop-card-content {
            flex: 1;
        }

        .laptop-card img {
            width: 100%;
            height: 200px;
            object-fit: contain;
            border-radius: 5px;
            margin-bottom: 20px;
            transition: transform 0.5s ease;
            filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.5));
        }

        .laptop-card:hover img {
            transform: scale(1.05);
        }

        .laptop-card h3 {
            font-size: 1.5em;
            color: white;
            margin-bottom: 15px;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
            position: relative;
            padding-bottom: 10px;
        }

        .laptop-card h3:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 2px;
            background: var(--asus-red);
            transition: width 0.3s ease;
        }

        .laptop-card:hover h3:after {
            width: 100px;
        }

        .laptop-card ul {
            text-align: left;
            padding-left: 0;
            list-style: none;
            margin-top: 15px;
        }

        .laptop-card ul li {
            font-size: 0.95em;
            padding: 8px 0;
            color: rgba(255, 255, 255, 0.8);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-left: 25px;
            position: relative;
            transition: all 0.3s ease;
        }

        .laptop-card ul li:hover {
            color: white;
            padding-left: 30px;
        }

        .laptop-card ul li::before {
            content: '\\2022';
            color: var(--asus-red);
            font-weight: bold;
            font-size: 1.2em;
            position: absolute;
            left: 5px;
            top: 5px;
            transition: all 0.3s ease;
        }

        .laptop-card ul li:hover::before {
            transform: scale(1.3);
            left: 8px;
        }

        /* Price and Button */
        .laptop-price {
            font-size: 1.3em;
            font-weight: 700;
            color: var(--asus-red);
            margin: 20px 0;
            text-align: center;
        }

        .laptop-btn-container {
            margin-top: auto;
            padding-top: 15px;
        }

        .laptop-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background: var(--asus-red);
            color: white;
            text-align: center;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            border: none;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9em;
        }

        .laptop-btn:hover {
            background: white;
            color: var(--asus-red);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
        }

        /* Footer Styles */
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

        .footer-section p,
        .footer-section ul {
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
            .asus-showroom h2 {
                font-size: 2em;
            }

            .laptop-card {
                padding: 20px;
            }

            .footer-content {
                grid-template-columns: 1fr;
            }

            .category-tabs {
                flex-direction: column;
                align-items: center;
            }

            .category-tab {
                width: 80%;
                text-align: center;
            }
        }
    </style>
</head>

<body>
    <!-- Header with Animated Logo -->
    <header class="header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo" class="logo" />
        <h1>ASUS Premium Showroom</h1>
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
                    <li><a href="./service3.py">Service</a></li>
                    <li class="active"><a href="./models.py">Laptops</a></li>
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

    <section class="asus-showroom">
        <h2>ASUS 2025 Laptop Collection</h2>

        <!-- Category Tabs -->
        <div class="category-tabs">
            <div class="category-tab active" data-category="gaming">Gaming</div>
            <div class="category-tab" data-category="business">Business</div>
            <div class="category-tab" data-category="ultraportable">Ultraportable</div>
            <div class="category-tab" data-category="creators">Creators</div>
        </div>

        <!-- Gaming Laptops -->
        <div class="category-section active" id="gaming">
            <h3 class="section-title">Gaming Series</h3>
            <div class="laptop-grid">
                <!-- ROG Zephyrus G16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/ROG Zephyrus G16.jpg" alt="ROG Zephyrus G16">
                        <h3>ROG Zephyrus G16</h3>
                        <ul>
                            <li>🎮 Intel Core i9-14900HX</li>
                            <li>🖥️ NVIDIA RTX 4090 (16GB)</li>
                            <li>🖥️ 16" QHD+ 240Hz Nebula HDR</li>
                            <li>🧠 32GB DDR5 RAM</li>
                            <li>💾 2TB PCIe 4.0 SSD</li>
                            <li>⌨️ Per-key RGB keyboard</li>
                            <li>🧊 Advanced cooling system</li>
                        </ul>
                        <div class="laptop-price">₹2,49,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ROG Flow Z13 (2025) -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/ROG Flow Z13.jpg" alt="ROG Flow Z13">
                        <h3>ROG Flow Z13 (2025)</h3>
                        <ul>
                            <li>🎮 AMD Ryzen AI Max+ 395 (16 cores)</li>
                            <li>🖥️ AMD Radeon 8060S Graphics</li>
                            <li>🖥️ 13" 2.5K Touchscreen (180Hz/3ms)</li>
                            <li>🧠 32GB LPDDR5X-8000 unified memory</li>
                            <li>💾 1TB PCIe 4.0 SSD</li>
                            <li>🔋 70Wh battery (10+ hours)</li>
                        </ul>
                        <div class="laptop-price">₹1,79,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- TUF Gaming A18 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/asus tuf a15.jpg" alt="TUF Gaming A18">
                        <h3>TUF Gaming A18</h3>
                        <ul>
                            <li>🎮 AMD Ryzen 9 7945HX3D</li>
                            <li>🖥️ NVIDIA RTX 4080 (12GB)</li>
                            <li>🖥️ 18" FHD 165Hz Anti-glare</li>
                            <li>🧠 16GB DDR5 RAM</li>
                            <li>💾 1TB PCIe 4.0 SSD</li>
                            <li>🛡️ Military-grade durability</li>
                            <li>🔌 330W power adapter</li>
                        </ul>
                        <div class="laptop-price">₹1,89,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ROG Strix SCAR 18 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/ROG Strix g18.jpg" alt="ROG Strix SCAR 18">
                        <h3>ROG Strix SCAR 18</h3>
                        <ul>
                            <li>🎮 Intel Core i9-14900HX</li>
                            <li>🖥️ NVIDIA RTX 4090 (16GB)</li>
                            <li>🖥️ 18" QHD+ 240Hz Mini-LED</li>
                            <li>🧠 64GB DDR5 RAM</li>
                            <li>💾 4TB PCIe 4.0 SSD (RAID 0)</li>
                            <li>🔑 Keystone 3 support</li>
                            <li>🎧 Hi-Res audio</li>
                        </ul>
                        <div class="laptop-price">₹3,29,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Gaming V16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/vivobookV16.jpg" alt="ASUS Gaming V16">
                        <h3>Gaming V16</h3>
                        <ul>
                            <li>🎮 NVIDIA GeForce RTX 4050 GPU</li>
                            <li>🧠 Intel Core Ultra 5 processor</li>
                            <li>🖥️ 16" FHD display</li>
                            <li>💾 16GB RAM, 512GB SSD</li>
                            <li>🎧 DTS:X Ultra audio</li>
                            <li>⌨️ RGB gaming keyboard</li>
                            <li>🔄 144Hz refresh rate</li>
                        </ul>
                        <div class="laptop-price">₹1,29,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- TUF Gaming A15 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/asus tuf a15.jpg" alt="TUF Gaming A15">
                        <h3>TUF Gaming A15</h3>
                        <ul>
                            <li>🧱 AMD Ryzen 7 260, RTX 5070 GPU</li>
                            <li>🖥️ 16" 2.5K 165Hz display</li>
                            <li>🛡️ Military-grade durability</li>
                            <li>🧊 Advanced cooling system</li>
                            <li>⚡ 90Wh battery</li>
                            <li>🔌 330W power adapter</li>
                            <li>⌨️ RGB backlit keyboard</li>
                        </ul>
                        <div class="laptop-price">₹1,59,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Business Laptops -->
        <div class="category-section" id="business">
            <h3 class="section-title">Business Series</h3>
            <div class="laptop-grid">
                <!-- ExpertBook B9 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/b9.png" alt="ExpertBook B9">
                        <h3>ExpertBook B9</h3>
                        <ul>
                            <li>💼 Intel vPro® Core Ultra 7</li>
                            <li>🖥️ 14" WUXGA anti-glare</li>
                            <li>🧠 32GB LPDDR5X RAM</li>
                            <li>💾 2TB PCIe SSD</li>
                            <li>🛡️ MIL-STD-810H certified</li>
                            <li>🔋 92Wh battery</li>
                            <li>🔒 Enhanced security</li>
                        </ul>
                        <div class="laptop-price">₹1,79,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook A14 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/zenbook a14.jpg" alt="ASUS Zenbook A14">
                        <h3>Zenbook A14</h3>
                        <ul>
                            <li>🌟 Ultra-lightweight (under 1kg)</li>
                            <li>🔋 70Wh battery, Snapdragon X chipset</li>
                            <li>🖥️ 14" Lumina OLED display</li>
                            <li>🧠 Copilot+ AI features</li>
                            <li>⚡ 32GB LPDDR5X RAM</li>
                            <li>💾 2TB PCIe 4.0 SSD</li>
                            <li>📶 Wi-Fi 7 connectivity</li>
                        </ul>
                        <div class="laptop-price">₹1,49,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Vivobook 14 Flip -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/vivobook 14  flip.jpg" alt="Vivobook 14 Flip">
                        <h3>Vivobook 14 Flip</h3>
                        <ul>
                            <li>🔄 360° hinge design</li>
                            <li>🖥️ 14" Lumina OLED touchscreen</li>
                            <li>🧠 Intel Core Ultra 7 processor</li>
                            <li>✍️ ASUS Pen 2.0 support</li>
                            <li>📷 5MP front camera</li>
                            <li>🔋 70Wh battery</li>
                            <li>⚖️ 1.3kg lightweight</li>
                        </ul>
                        <div class="laptop-price">₹89,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ExpertBook B5 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/expertbook-b5.jpg" alt="ExpertBook B5">
                        <h3>ExpertBook B5 (2025)</h3>
                        <ul>
                            <li>💼 Intel Core Ultra 7 vPro (24-core) / AMD Ryzen AI 7 PRO</li>
                            <li>🖥️ Intel Arc Graphics / AMD Radeon</li>
                            <li>🖥️ 14" 2.5K Anti-glare (144Hz, 400 nits)</li>
                            <li>🧠 64GB DDR5 RAM (upgradable)</li>
                            <li>💾 3TB Dual PCIe 4.0 SSD (RAID support)</li>
                            <li>🔒 Military-grade durability & TPM 2.0</li>
                            <li>🔋 70Wh battery (18+ hours)</li>
                        </ul>
                        <div class="laptop-price">₹1,49,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ProArt Studiobook 16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/ProArt Studiobook 16.png" alt="ProArt Studiobook 16">
                        <h3>ProArt Studiobook 16</h3>
                        <ul>
                            <li>💼 Intel Core Ultra 9 185H</li>
                            <li>🖥️ NVIDIA RTX 5000 Ada (16GB)</li>
                            <li>🖥️ 16" 4K OLED 120Hz</li>
                            <li>🧠 64GB DDR5 RAM</li>
                            <li>💾 4TB SSD</li>
                            <li>🎨 ASUS Dial for control</li>
                            <li>🎯 Pantone validated</li>
                        </ul>
                        <div class="laptop-price">₹2,79,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ProArt P16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/proart-p16.jpg" alt="ProArt P16">
                        <h3>ProArt P16 (2025)</h3>
                        <ul>
                            <li>💼 Intel Core Ultra 9 / AMD Ryzen 9 9955HX</li>
                            <li>🖥️ NVIDIA RTX 5000 Ada GPU (16GB VRAM)</li>
                            <li>🖥️ 16" 4K OLED (120Hz, 550 nits)</li>
                            <li>🧠 128GB DDR5 ECC RAM</li>
                            <li>💾 8TB PCIe 5.0 SSD (RAID 0)</li>
                            <li>🎨 Calman-verified for color grading</li>
                            <li>🔋 90Wh battery (10+ hours)</li>
                        </ul>
                        <div class="laptop-price">₹2,99,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Vivobook 16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/vivobook 16.jpg" alt="ASUS Vivobook 16">
                        <h3>Vivobook 16</h3>
                        <ul>
                            <li>🖥️ 16" FHD IPS display</li>
                            <li>🧠 Snapdragon X processor</li>
                            <li>💾 Up to 16GB RAM</li>
                            <li>🔋 Up to 17 hours battery life</li>
                            <li>📦 512GB SSD</li>
                            <li>🔌 Fast charging support</li>
                            <li>🎤 AI noise cancellation</li>
                        </ul>
                        <div class="laptop-price">₹74,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Ultraportable Laptops -->
        <div class="category-section" id="ultraportable">
            <h3 class="section-title">Ultraportable Series</h3>
            <div class="laptop-grid">
                <!-- Zenbook S 13 OLED -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/Zenbook S 13 OLED.jpg" alt="Zenbook S 13 OLED">
                        <h3>Zenbook S 13 OLED</h3>
                        <ul>
                            <li>✈️ AMD Ryzen 7 7840U</li>
                            <li>🖥️ 13.3" 2.8K OLED 90Hz</li>
                            <li>🧠 16GB LPDDR5 RAM</li>
                            <li>💾 1TB SSD</li>
                            <li>⚖️ 1kg lightweight</li>
                            <li>🔋 18-hour battery</li>
                            <li>📶 Wi-Fi 6E</li>
                        </ul>
                        <div class="laptop-price">₹1,19,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Vivobook S14 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/zenbook a14.jpg" alt="ASUS Vivobook S14">
                        <h3>Vivobook S14</h3>
                        <ul>
                            <li>🖥️ 14" Lumina OLED display</li>
                            <li>🧠 Intel Core Ultra 7 processor</li>
                            <li>🔊 Harman Kardon-certified speakers</li>
                            <li>🔋 75Wh battery</li>
                            <li>💾 16GB LPDDR5X RAM</li>
                            <li>📦 1TB PCIe 4.0 SSD</li>
                            <li>🎨 Multiple color options</li>
                        </ul>
                        <div class="laptop-price">₹99,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook 14X OLED -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/Zenbook 14X OLED.png" alt="Zenbook 14X OLED">
                        <h3>Zenbook 14X OLED</h3>
                        <ul>
                            <li>✈️ Intel Core Ultra 7 155H</li>
                            <li>🖥️ 14" 3K 120Hz OLED touch</li>
                            <li>🧠 32GB LPDDR5X RAM</li>
                            <li>💾 2TB SSD</li>
                            <li>🎵 Harman Kardon audio</li>
                            <li>🔢 NumberPad 2.0</li>
                            <li>⚖️ 1.2kg lightweight</li>
                        </ul>
                        <div class="laptop-price">₹1,39,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Vivobook S 14 Flip -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/Vivobook S 14 Flip.png" alt="Vivobook S 14 Flip">
                        <h3>Vivobook S 14 Flip</h3>
                        <ul>
                            <li>✈️ Intel Core Ultra 5 125U</li>
                            <li>🖥️ 14" FHD 360° touch</li>
                            <li>🧠 16GB RAM</li>
                            <li>💾 512GB SSD</li>
                            <li>✍️ ASUS Pen 2.0</li>
                            <li>⚖️ 1.3kg lightweight</li>
                            <li>🔋 Fast charging</li>
                        </ul>
                        <div class="laptop-price">₹79,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook S16 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/zenbook 16.jpg" alt="ASUS Zenbook S16">
                        <h3>Zenbook S16</h3>
                        <ul>
                            <li>💼 16" 3K OLED display</li>
                            <li>🧠 AMD Ryzen AI 7 350 processor</li>
                            <li>🧠 Copilot+ AI features</li>
                            <li>⚡ 120Hz refresh rate</li>
                            <li>📦 2TB PCIe 5.0 SSD</li>
                            <li>📷 1080p IR camera</li>
                            <li>🔋 18-hour battery life</li>
                        </ul>
                        <div class="laptop-price">₹1,59,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook 14 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/zenbook 14.jpg" alt="ASUS Zenbook 14">
                        <h3>Zenbook 14</h3>
                        <ul>
                            <li>🖥️ 14" 3K OLED display</li>
                            <li>🧠 Intel Core Ultra 9 processor</li>
                            <li>💾 Up to 32GB RAM</li>
                            <li>📦 Up to 1TB SSD</li>
                            <li>🔋 63Wh battery</li>
                            <li>📶 Thunderbolt 5 ports</li>
                            <li>🎨 Premium aluminum chassis</li>
                        </ul>
                        <div class="laptop-price">₹1,29,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Creator Laptops -->
        <div class="category-section" id="creators">
            <h3 class="section-title">Creator Series</h3>
            <div class="laptop-grid">
                <!-- ProArt Studiobook Pro 16 OLED -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/ProArt Studiobook Pro 16 OLED.png" alt="ProArt Studiobook Pro 16 OLED">
                        <h3>ProArt Studiobook Pro 16</h3>
                        <ul>
                            <li>🎨 Intel Core Ultra 9 185H</li>
                            <li>🖥️ NVIDIA RTX 4000 Ada (12GB)</li>
                            <li>🖥️ 16" 4K OLED 120Hz</li>
                            <li>🧠 64GB DDR5 RAM</li>
                            <li>💾 4TB SSD</li>
                            <li>🎛️ ASUS Dial control</li>
                            <li>🎯 Built-in colorimeter</li>
                        </ul>
                        <div class="laptop-price">₹2,89,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook Pro 16X OLED -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/Zenbook Pro 16X OLED.png" alt="Zenbook Pro 16X OLED">
                        <h3>Zenbook Pro 16X OLED</h3>
                        <ul>
                            <li>🎨 Intel Core Ultra 9 185H</li>
                            <li>🖥️ NVIDIA RTX 4080 (12GB)</li>
                            <li>🖥️ 16" 4K OLED 120Hz touch</li>
                            <li>🧠 32GB DDR5 RAM</li>
                            <li>💾 2TB SSD</li>
                            <li>❄️ AAS Ultra cooling</li>
                            <li>🎵 Dolby Atmos</li>
                        </ul>
                        <div class="laptop-price">₹2,49,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Zenbook 14 OLED -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/zenbook-14-oled.jpg" alt="Zenbook 14 OLED">
                        <h3>Zenbook 14 OLED (2025)</h3>
                        <ul>
                            <li>💼 Intel Core Ultra 7 155H (24-core AI NPU)</li>
                            <li>🖥️ Intel Arc Graphics</li>
                            <li>🖥️ 14" 3K Lumina OLED (120Hz, 100% DCI-P3)</li>
                            <li>🧠 32GB LPDDR5X RAM</li>
                            <li>💾 2TB PCIe 4.0 SSD</li>
                            <li>📱 0.59" thin | 2.82 lbs</li>
                        </ul>
                        <div class="laptop-price">₹1,29,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- ExpertBook B5 -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/expertbook-b5.jpg" alt="ExpertBook B5">
                        <h3>ExpertBook B5 (2025)</h3>
                        <ul>
                            <li>💼 Intel Core Ultra 7 vPro / AMD Ryzen AI 7 PRO</li>
                            <li>🖥️ Intel Arc / AMD Radeon Graphics</li>
                            <li>🖥️ 14" 2.5K Anti-glare (144Hz, 400 nits)</li>
                            <li>🧠 64GB DDR5 (upgradable)</li>
                            <li>💾 3TB Dual PCIe 4.0 SSD (RAID support)</li>
                            <li>🔒 TPM 2.0 + Smart Card Reader</li>
                        </ul>
                        <div class="laptop-price">₹1,49,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>

                <!-- Vivobook Pro 16X -->
                <div class="laptop-card">
                    <div class="laptop-card-content">
                        <img src="./img/Vivobook Pro 16X.png" alt="Vivobook Pro 16X">
                        <h3>Vivobook Pro 16X</h3>
                        <ul>
                            <li>🎨 AMD Ryzen 9 7945HX</li>
                            <li>🖥️ NVIDIA RTX 4070 (8GB)</li>
                            <li>🖥️ 16" WQXGA 165Hz</li>
                            <li>🧠 32GB DDR5 RAM</li>
                            <li>💾 1TB SSD</li>
                            <li>🎯 Pantone validated</li>
                            <li>⌨️ ErgoLift hinge</li>
                        </ul>
                        <div class="laptop-price">₹1,89,990</div>
                    </div>
                    <div class="laptop-btn-container">
                        <a href="./bookinglap.py" class="laptop-btn">Book Now</a>
                    </div>
                </div>
            </div>
        </div>
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
                <ul>
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

        // Add animation when scrolling
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.laptop-card').forEach(card => {
            card.style.opacity = 0;
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });

        // Category tab functionality
        document.querySelectorAll('.category-tab').forEach(tab => {
            tab.addEventListener('click', function () {
                // Remove active class from all tabs and sections
                document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.category-section').forEach(s => s.classList.remove('active'));

                // Add active class to clicked tab
                this.classList.add('active');

                // Show corresponding section
                const category = this.getAttribute('data-category');
                document.getElementById(category).classList.add('active');

                // Scroll to section
                document.getElementById(category).scrollIntoView({ behavior: 'smooth' });
            });
        });
    </script>
</body>

</html>
""")