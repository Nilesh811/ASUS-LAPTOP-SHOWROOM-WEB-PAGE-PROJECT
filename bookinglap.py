#!C:/Python/python.exe
import smtplib
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
    <title>ASUS Laptop Booking</title>
    <style>
        :root {
            --primary-color: #0033a0;
            --secondary-color: #f5f5f5;
            --accent-color: #e0e0e0;
            --text-color: #333333;
            --success-color: #4CAF50;
            --danger-color: #F44336;
            --rog-red: #ff0028;
            --tuf-yellow: #ffcc00;
            --zenbook-blue: #0077c8;
            --vivobook-green: #00a88e;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #000;
            color: var(--text-color);
            padding: 20px;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                linear-gradient(45deg, rgba(0, 51, 160, 0.1) 0%, rgba(0, 0, 0, 0.9) 100%),
                url('./img/asus-rog-3840x2160-11677.jpg') center/cover no-repeat;
            z-index: -1;
            animation: gradientShift 15s ease infinite alternate;
        }

        @keyframes gradientShift {
            0% {
                background-position: 0% 50%;
                background-size: 150% 150%;
            }

            50% {
                background-position: 100% 50%;
                background-size: 200% 200%;
            }

            100% {
                background-position: 0% 50%;
                background-size: 150% 150%;
            }
        }

        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            background: rgba(0, 51, 160, 0.7);
            border-radius: 50%;
            animation: float linear infinite;
            filter: blur(1px);
        }

        .particle.asus-logo {
            background: transparent;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path fill="%230033a0" d="M50 0L0 50l50 50 50-50z"/></svg>');
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.3;
        }

        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg) scale(1);
                opacity: 0;
            }

            10% {
                opacity: 0.5;
            }

            90% {
                opacity: 0.5;
            }

            100% {
                transform: translateY(-20vh) rotate(360deg) scale(1.5);
                opacity: 0;
            }
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid var(--primary-color);
            box-shadow: 0 0 20px rgba(0, 51, 160, 0.5);
            animation: pulse 6s infinite alternate, floatHeader 8s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(to bottom right,
                    transparent 0%,
                    rgba(0, 51, 160, 0.1) 20%,
                    transparent 40%,
                    transparent 60%,
                    rgba(255, 0, 40, 0.1) 80%,
                    transparent 100%);
            animation: shine 8s linear infinite;
            transform: rotate(30deg);
        }

        @keyframes shine {
            0% {
                transform: translateX(-100%) rotate(30deg);
            }

            100% {
                transform: translateX(100%) rotate(30deg);
            }
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 20px rgba(0, 51, 160, 0.5);
            }

            50% {
                box-shadow: 0 0 30px rgba(0, 51, 160, 0.8), 0 0 15px rgba(255, 0, 40, 0.6);
            }

            100% {
                box-shadow: 0 0 20px rgba(0, 51, 160, 0.5);
            }
        }

        @keyframes floatHeader {

            0%,
            100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-10px);
            }
        }

        .header img {
            height: 80px;
            margin-bottom: 15px;
            filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
            animation: logoGlow 4s ease-in-out infinite alternate;
        }

        @keyframes logoGlow {
            0% {
                filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.3));
            }

            100% {
                filter: drop-shadow(0 0 15px rgba(0, 51, 160, 0.8));
            }
        }

        .header h1 {
            color: white;
            margin-bottom: 10px;
            font-size: 2rem;
            text-shadow: 0 0 10px rgba(0, 51, 160, 0.8);
            animation: textGlow 3s ease-in-out infinite alternate;
        }

        @keyframes textGlow {
            0% {
                text-shadow: 0 0 5px rgba(0, 51, 160, 0.5);
            }

            100% {
                text-shadow: 0 0 15px rgba(0, 51, 160, 0.9), 0 0 5px rgba(255, 255, 255, 0.5);
            }
        }

        .header p {
            color: #aaa;
            font-size: 1.1rem;
        }

        .form-container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(0, 51, 160, 0.5);
            border: 1px solid var(--primary-color);
            backdrop-filter: blur(5px);
            transition: all 0.5s ease;
            animation: formEntrance 1s ease-out;
        }

        @keyframes formEntrance {
            0% {
                opacity: 0;
                transform: translateY(50px);
            }

            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .form-section {
            margin-bottom: 25px;
            position: relative;
        }

        .form-section h2 {
            color: white;
            margin-bottom: 15px;
            font-size: 1.5rem;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 8px;
            text-shadow: 0 0 5px rgba(0, 51, 160, 0.8);
        }

        .form-row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -10px 15px;
        }

        .form-group {
            flex: 1 0 200px;
            margin: 0 10px 15px;
            position: relative;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #ddd;
        }

        .required:after {
            content: " *";
            color: var(--danger-color);
        }

        input,
        select,
        textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--primary-color);
            border-radius: 5px;
            font-size: 16px;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            transition: all 0.3s;
        }

        input:focus,
        select:focus,
        textarea:focus {
            outline: none;
            border-color: var(--rog-red);
            box-shadow: 0 0 10px rgba(255, 0, 40, 0.5);
            background-color: rgba(0, 0, 0, 0.7);
            transform: scale(1.02);
        }

        .laptop-selection {
            max-height: 500px;
            overflow-y: auto;
            padding-right: 10px;
            border: 1px solid var(--primary-color);
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            background: rgba(0, 0, 0, 0.5);
        }

        .laptop-option {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(0, 51, 160, 0.5);
            transition: all 0.3s;
            position: relative;
        }

        .laptop-option:hover {
            transform: translateX(5px);
            background: rgba(0, 51, 160, 0.1);
        }

        .laptop-option:last-child {
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }

        .laptop-image {
            width: 120px;
            height: 120px;
            object-fit: contain;
            margin-right: 20px;
            border: 1px solid var(--primary-color);
            border-radius: 5px;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 5px;
            transition: all 0.3s;
        }

        .laptop-option:hover .laptop-image {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
        }

        .laptop-details {
            flex: 1;
        }

        .laptop-details h3 {
            color: white;
            margin-bottom: 5px;
            font-size: 1.2rem;
        }

        .laptop-specs {
            font-size: 14px;
            color: #aaa;
            margin-bottom: 10px;
        }

        .laptop-price {
            font-weight: bold;
            font-size: 18px;
            color: var(--rog-red);
            text-shadow: 0 0 5px rgba(255, 0, 40, 0.3);
        }

        .radio-group {
            display: flex;
            align-items: center;
            margin-left: 20px;
        }

        .radio-group input {
            width: auto;
            margin-right: 10px;
            accent-color: var(--rog-red);
        }

        .radio-group label {
            color: white;
            cursor: pointer;
        }

        .btn {
            background: linear-gradient(45deg, var(--primary-color), var(--rog-red));
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            background: linear-gradient(45deg, var(--rog-red), var(--primary-color));
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }

        .btn:active {
            transform: translateY(1px);
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg,
                    transparent,
                    rgba(255, 255, 255, 0.2),
                    transparent);
            transition: 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn-block {
            display: block;
            width: 100%;
        }

        .payment-options {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .payment-btn {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--primary-color);
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
            font-size: 16px;
        }

        .payment-btn:hover {
            background: rgba(0, 51, 160, 0.3);
            transform: translateY(-2px);
        }

        .payment-btn.active {
            background: linear-gradient(45deg, var(--primary-color), var(--rog-red));
            border-color: var(--rog-red);
            box-shadow: 0 0 10px rgba(255, 0, 40, 0.5);
        }

        .payment-btn i {
            font-size: 20px;
        }



        /* Series-specific styling */
        .rog {
            border-left: 4px solid var(--rog-red);
        }

        .tuf {
            border-left: 4px solid var(--tuf-yellow);
        }

        .zenbook {
            border-left: 4px solid var(--zenbook-blue);
        }

        .vivobook {
            border-left: 4px solid var(--vivobook-green);
        }

        .expertbook {
            border-left: 4px solid #7d00c4;
        }

        .proart {
            border-left: 4px solid #ff7700;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--rog-red);
        }

        /* ASUS logo animation */
        .asus-logo-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            animation: fadeOut 1s ease-out 2s forwards;
        }

        .asus-logo-animation img {
            width: 200px;
            animation: logoPulse 1.5s ease-in-out infinite alternate;
        }

        @keyframes logoPulse {
            0% {
                transform: scale(1);
                opacity: 0.7;
                filter: drop-shadow(0 0 5px rgba(0, 51, 160, 0.5));
            }

            100% {
                transform: scale(1.2);
                opacity: 1;
                filter: drop-shadow(0 0 20px rgba(0, 51, 160, 0.9));
            }
        }

        @keyframes fadeOut {
            0% {
                opacity: 1;
            }

            100% {
                opacity: 0;
                visibility: hidden;
            }
        }

        /* Ripple effect */
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0);
            animation: ripple 1s linear;
            pointer-events: none;
        }

        @keyframes ripple {
            to {
                transform: scale(2.5);
                opacity: 0;
            }
        }

        @media (max-width: 768px) {
            .form-row {
                flex-direction: column;
            }

            .form-group {
                flex: 1 0 auto;
            }

            .laptop-option {
                flex-direction: column;
                align-items: flex-start;
            }

            .laptop-image {
                margin-right: 0;
                margin-bottom: 15px;
                width: 100%;
                height: auto;
                max-width: 200px;
            }

            .radio-group {
                margin-left: 0;
                margin-top: 15px;
                width: 100%;
                justify-content: flex-end;
            }

            .header h1 {
                font-size: 1.5rem;
            }

            .header img {
                height: 60px;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>

<body>
    <div class="asus-logo-animation">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
    </div>

    <div class="particles" id="particles"></div>

    <div class="header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
        <h1>ASUS Laptop Booking</h1>
        <p>Experience innovation with ASUS's premium laptop lineup</p>
    </div>

    <div class="form-container">
        <form id="bookingForm" name="profile" method="post" enctype="multipart/form-data">
            <div class="form-section">
                <h2>Personal Information</h2>
                <div class="form-row">
                    <div class="form-group">
                        <label for="name" class="required">Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email" class="required">Email</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="phone" class="required">Phone</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label for="address">Address</label>
                        <input type="text" id="address" name="address">
                    </div>
                </div>
            </div>

            <div class="form-section">
                <h2>Laptop Selection</h2>
                <p style="color: #aaa;">Choose from our premium ASUS laptop lineup:</p>

          <div class="form-group">
    <label for="laptopSelect" class="required">Select Laptop Model</label>
    <select id="laptopSelect" name="laptopselect" required>
        <!-- ROG Series -->
        <option value="ROG Zephyrus G14 (2023)" data-img="img/ROG Zephyrus G14.jpg" data-specs="AMD Ryzen 9 7940HS | RTX 4060 | 32GB DDR5 | 1TB SSD | 14&quot; QHD 165Hz" data-price="₹1,69,990" data-series="rog" selected>
            ROG Zephyrus G14 (2023) - ₹1,69,990
        </option>
        <option value="ROG Strix Scar 17" data-img="./img/ROG Strix g17.jpg" data-specs="Intel i9-13980HX | RTX 4090 | 32GB DDR5 | 2TB SSD | 16&quot; Mini LED 240Hz" data-price="₹3,49,990" data-series="rog">
            ROG Strix Scar 17 - ₹3,49,990
        </option>
        <option value="ROG Zephyrus G16" data-img="./img/ROG Zephyrus G16.jpg" data-specs="Intel Core i9-14900HX | RTX 4090 | 32GB DDR5 | 2TB SSD | 16&quot; QHD+ 240Hz" data-price="₹2,49,990" data-series="rog">
            ROG Zephyrus G16 - ₹2,49,990
        </option>
        <option value="ROG Strix SCAR 18" data-img="./img/ROG Strix g18.jpg" data-specs="Intel Core i9-14900HX | RTX 4090 | 64GB DDR5 | 4TB SSD | 18&quot; QHD+ 240Hz" data-price="₹3,29,990" data-series="rog">
            ROG Strix SCAR 18 - ₹3,29,990
        </option>
        <option value="ROG Flow Z13 (2025)" data-img="./img/ROG Flow Z13.jpg" data-specs="AMD Ryzen AI Max+ 395 | Radeon 8060S | 32GB LPDDR5X | 1TB SSD | 13&quot; 2.5K Touch" data-price="₹1,79,990" data-series="rog">
            ROG Flow Z13 (2025) - ₹1,79,990
        </option>

        <!-- TUF Series -->
        <option value="TUF Gaming F15" data-img="./img/tuf gamminf f 15.jpg" data-specs="Intel i7-12700H | RTX 3060 | 16GB DDR4 | 1TB SSD | 15.6&quot; FHD 144Hz" data-price="₹1,19,990" data-series="tuf">
            TUF Gaming F15 - ₹1,19,990
        </option>
        <option value="TUF Gaming A18" data-img="./img/asus tuf a15.jpg" data-specs="AMD Ryzen 9 7945HX3D | RTX 4080 | 16GB DDR5 | 1TB SSD | 18&quot; FHD 165Hz" data-price="₹1,89,990" data-series="tuf">
            TUF Gaming A18 - ₹1,89,990
        </option>
        <option value="TUF Gaming A15" data-img="./img/asus tuf a15.jpg" data-specs="AMD Ryzen 7 260 | RTX 5070 | 16GB DDR5 | 1TB SSD | 16&quot; 2.5K 165Hz" data-price="₹1,59,990" data-series="tuf">
            TUF Gaming A15 - ₹1,59,990
        </option>

        <!-- ZenBook Series -->
        <option value="ZenBook 14 OLED" data-img="./img/zenbook 14.jpg" data-specs="Intel i7-1360P | Iris Xe | 16GB LPDDR5 | 1TB SSD | 14&quot; 2.8K OLED" data-price="₹1,29,990" data-series="zenbook">
            ZenBook 14 OLED - ₹1,29,990
        </option>
        <option value="ZenBook Pro 16X OLED" data-img="./img/zenbook 16.jpg" data-specs="Intel i9-13900H | RTX 4070 | 32GB DDR5 | 2TB SSD | 16&quot; 4K OLED" data-price="₹2,59,990" data-series="zenbook">
            ZenBook Pro 16X OLED - ₹2,59,990
        </option>
        <option value="Zenbook S 13 OLED" data-img="./img/Zenbook S 13 OLED.jpg" data-specs="AMD Ryzen 7 7840U | 16GB LPDDR5 | 1TB SSD | 13.3&quot; 2.8K OLED" data-price="₹1,19,990" data-series="zenbook">
            Zenbook S 13 OLED - ₹1,19,990
        </option>
        <option value="Zenbook A14" data-img="./img/zenbook a14.jpg" data-specs="Snapdragon X | 32GB LPDDR5X | 2TB SSD | 14&quot; Lumina OLED" data-price="₹1,49,990" data-series="zenbook">
            Zenbook A14 - ₹1,49,990
        </option>
        <option value="Zenbook 14X OLED" data-img="./img/Zenbook 14X OLED.png" data-specs="Intel Core Ultra 7 | 32GB LPDDR5X | 2TB SSD | 14&quot; 3K OLED" data-price="₹1,39,990" data-series="zenbook">
            Zenbook 14X OLED - ₹1,39,990
        </option>
        <option value="Zenbook S16" data-img="./img/zenbook 16.jpg" data-specs="AMD Ryzen AI 7 | 16GB RAM | 2TB SSD | 16&quot; 3K OLED" data-price="₹1,59,990" data-series="zenbook">
            Zenbook S16 - ₹1,59,990
        </option>
        <option value="Zenbook 14" data-img="./img/zenbook 14.jpg" data-specs="Intel Core Ultra 9 | 32GB RAM | 1TB SSD | 14&quot; 3K OLED" data-price="₹1,29,990" data-series="zenbook">
            Zenbook 14 - ₹1,29,990
        </option>
        <option value="Zenbook 14 OLED (2025)" data-img="./img/zenbook-14-oled.jpg" data-specs="Intel Core Ultra 7 155H | Intel Arc | 32GB LPDDR5X | 2TB SSD | 14&quot; 3K OLED" data-price="₹1,29,990" data-series="zenbook">
            Zenbook 14 OLED (2025) - ₹1,29,990
        </option>

        <!-- Vivobook Series -->
        <option value="VivoBook 14 Flip" data-img="./img/vivobook 14  flip.jpg" data-specs="Intel Core i5-1235U | 8GB DDR4 | 512GB SSD | 15.6&quot; FHD" data-price="₹59,990" data-series="vivobook">
            VivoBook 14 Flip - ₹59,990
        </option>
        <option value="VivoBook V16" data-img="./img/vivobookV16.jpg" data-specs="AMD Ryzen 7 5800H | 16GB DDR4 | 1TB SSD | 14&quot; FHD Touch 360°" data-price="₹89,990" data-series="vivobook">
            VivoBook V16 - ₹89,990
        </option>
        <option value="Gaming V16" data-img="./img/vivobookV16.jpg" data-specs="Intel Core Ultra 5 | RTX 4050 | 16GB RAM | 512GB SSD | 16&quot; FHD" data-price="₹1,29,990" data-series="vivobook">
            Gaming V16 - ₹1,29,990
        </option>
        <option value="Vivobook S14" data-img="./img/zenbook a14.jpg" data-specs="Intel Core Ultra 7 | 16GB LPDDR5X | 1TB SSD | 14&quot; Lumina OLED" data-price="₹99,990" data-series="vivobook">
            Vivobook S14 - ₹99,990
        </option>
        <option value="Vivobook S 14 Flip" data-img="./img/Vivobook S 14 Flip.png" data-specs="Intel Core Ultra 5 | 16GB RAM | 512GB SSD | 14&quot; FHD Touch" data-price="₹79,990" data-series="vivobook">
            Vivobook S 14 Flip - ₹79,990
        </option>
        <option value="Vivobook 16" data-img="./img/vivobook 16.jpg" data-specs="Snapdragon X | 16GB RAM | 512GB SSD | 16&quot; FHD IPS" data-price="₹74,990" data-series="vivobook">
            Vivobook 16 - ₹74,990
        </option>
        <option value="Vivobook Pro 16X" data-img="./img/Vivobook Pro 16X.png" data-specs="AMD Ryzen 9 | RTX 4070 | 32GB DDR5 | 1TB SSD | 16&quot; WQXGA" data-price="₹1,89,990" data-series="vivobook">
            Vivobook Pro 16X - ₹1,89,990
        </option>

        <!-- ExpertBook Series -->
        <option value="ExpertBook B9" data-img="./img/b9.png" data-specs="Intel i7-1260P | 16GB LPDDR5 | 1TB SSD | 14&quot; FHD | Military Grade" data-price="₹1,49,990" data-series="expertbook">
            ExpertBook B9 - ₹1,49,990
        </option>
        <option value="ExpertBook B5 (2025)" data-img="./img/expertbook-b5.jpg" data-specs="Intel Core Ultra 7 vPro/AMD Ryzen AI 7 PRO | 64GB DDR5 | 3TB SSD | 14&quot; 2.5K" data-price="₹1,49,990" data-series="expertbook">
            ExpertBook B5 (2025) - ₹1,49,990
        </option>

        <!-- ProArt Series -->
        <option value="ProArt Studiobook 16" data-img="./img/pro.png" data-specs="AMD Ryzen 9 7945HX | RTX 4070 | 32GB DDR5 | 2TB SSD | 16&quot; 4K OLED" data-price="₹2,99,990" data-series="proart">
            ProArt Studiobook 16 - ₹2,99,990
        </option>
        <option value="ProArt Studiobook Pro 16" data-img="./img/ProArt Studiobook Pro 16 OLED.png" data-specs="Intel Core Ultra 9 | RTX 4000 Ada | 64GB DDR5 | 4TB SSD | 16&quot; 4K OLED" data-price="₹2,89,990" data-series="proart">
            ProArt Studiobook Pro 16 - ₹2,89,990
        </option>
        <option value="ProArt P16 (2025)" data-img="./img/proart-p16.jpg" data-specs="Intel Core Ultra 9/AMD Ryzen 9 | RTX 5000 Ada | 128GB DDR5 | 8TB SSD | 16&quot; 4K OLED" data-price="₹2,99,990" data-series="proart">
            ProArt P16 (2025) - ₹2,99,990
        </option>
    </select>
</div>

                <!-- Laptop Preview Section -->
                <div class="laptop-preview"
                    style="margin-top: 20px; display: flex; align-items: center; background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; border-left: 4px solid var(--rog-red);">
                    <img id="selectedLaptopImage" src="img/ROG Zephyrus G14.jpg" alt="Selected Laptop"
                        style="width: 120px; height: 120px; object-fit: contain; margin-right: 20px; border: 1px solid var(--primary-color); border-radius: 5px; background-color: rgba(255,255,255,0.9); padding: 5px;">
                    <div>
                        <h3 id="selectedLaptopName" style="color: white; margin-bottom: 5px;">ROG Zephyrus G14 (2023)
                        </h3>
                        <div id="selectedLaptopSpecs" style="font-size: 14px; color: #aaa; margin-bottom: 10px;">AMD
                            Ryzen 9 7940HS | RTX 4060 | 32GB DDR5 | 1TB SSD | 14" QHD 165Hz</div>
                        <div id="selectedLaptopPrice"
                            style="font-weight: bold; font-size: 18px; color: var(--rog-red); text-shadow: 0 0 5px rgba(255,0,40,0.3);">
                            ₹1,69,990</div>
                    </div>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="bookingDate" class="required">Preferred Booking Date</label>
                    <input type="date" id="bookingdate" name="bookingdate" required>
                </div>
            </div>

            <div class="form-section">
                <h2>Payment Information</h2>
                <div class="form-row">
                    <div class="form-group">
                        <label class="required">Payment Method</label>
                        <div class="payment-options">
                            <button type="button" id="cashOnDeliveryBtn" class="payment-btn active"
                                onclick="selectPayment('cash')">
                                <i class="fas fa-money-bill-wave"></i>
                                <span>Cash on Delivery</span>
                                <input type="radio" name="payment" value="cash" checked style="display: none;">
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" name="submit" class="btn btn-block">Book Now</button>
        </form>
    </div>

    <script>
        // Function to update laptop preview based on selection
        function updateLaptopPreview() {
            const selectElement = document.getElementById('laptopSelect');
            const selectedOption = selectElement.options[selectElement.selectedIndex];

            // Get data attributes from selected option
            const laptopName = selectedOption.value;
            const laptopImage = selectedOption.getAttribute('data-img');
            const laptopSpecs = selectedOption.getAttribute('data-specs');
            const laptopPrice = selectedOption.getAttribute('data-price');
            const laptopSeries = selectedOption.getAttribute('data-series');

            // Update preview elements
            document.getElementById('selectedLaptopImage').src = laptopImage;
            document.getElementById('selectedLaptopName').textContent = laptopName;
            document.getElementById('selectedLaptopSpecs').textContent = laptopSpecs;
            document.getElementById('selectedLaptopPrice').textContent = laptopPrice;

            // Update border color based on series
            const previewDiv = document.querySelector('.laptop-preview');
            previewDiv.style.borderLeftColor = getSeriesColor(laptopSeries);
        }

        // Helper function to get series color
        function getSeriesColor(series) {
            const colors = {
                'rog': '#ff0028',
                'tuf': '#ffcc00',
                'zenbook': '#0077c8',
                'vivobook': '#00a88e',
                'expertbook': '#7d00c4',
                'proart': '#ff7700'
            };
            return colors[series] || '#0033a0';
        }

        // Initialize the preview with default selected laptop
        document.addEventListener('DOMContentLoaded', function () {
            updateLaptopPreview();

            // Add event listener for dropdown change
            document.getElementById('laptopSelect').addEventListener('change', updateLaptopPreview);

            // Create particles
            createParticles();
        });

        // Create particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 30;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');

                // Random size between 5px and 15px
                const size = Math.random() * 10 + 5;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;

                // Random position
                particle.style.left = `${Math.random() * 100}%`;

                // Random animation duration between 10s and 20s
                const duration = Math.random() * 10 + 10;
                particle.style.animationDuration = `${duration}s`;

                // Random delay
                particle.style.animationDelay = `${Math.random() * 5}s`;

                // 10% chance to be an ASUS logo
                if (Math.random() < 0.1) {
                    particle.classList.add('asus-logo');
                    particle.style.width = `${size * 2}px`;
                    particle.style.height = `${size * 2}px`;
                }

                particlesContainer.appendChild(particle);
            }
        }

        function selectPayment(method) {
            // Set the radio button value
            document.querySelector(`input[name="payment"][value="${method}"]`).checked = true;

            // Update button styles
            const allPaymentBtns = document.querySelectorAll('.payment-btn');
            allPaymentBtns.forEach(btn => btn.classList.remove('active'));

            const activeBtn = document.getElementById(`${method}OnDeliveryBtn`) ||
                document.querySelector(`.payment-btn[onclick*="${method}"]`);
            if (activeBtn) activeBtn.classList.add('active');
        }
    </script>
</body>

</html>
""")

form = cgi.FieldStorage()

# Get form values (field names must match your HTML input 'name' attributes)
pname = form.getvalue("name")
pemailid = form.getvalue("email")
pphoneno = form.getvalue("phone")
paddress = form.getvalue("address")
plaptopselect = form.getvalue("laptopselect")
pbookingdate = form.getvalue("bookingdate")
psubmit = form.getvalue("submit")


if pname and pemailid and pphoneno and plaptopselect and pbookingdate:
    try:
        con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
        cur = con.cursor()

        q2 = """INSERT INTO booking(Name, Email_id, Phone, Address, Laptop_selection, Booking_date)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(q2, (pname, pemailid, pphoneno, paddress, plaptopselect, pbookingdate))
        con.commit()

        print("""
            <script>
                alert("Booking successful!");
                window.location.href = "index.py";
            </script>
        """)
    except Exception as e:
        print(f"<h3>Error: {e}</h3>")
    finally:
        fromaddr = "s.nilesh4321@gmail.com"
        password = "nudohwfqpcevrojw"
        toaddr = pemailid
        subject = "Order Booking Successfully"
        body = """Username: '%s' \n model: '%s' """ % (pname,plaptopselect )
        msg = """Subject:{}\n\n{}""".format(subject, body)
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg)
        server.quit()
        con.close()

