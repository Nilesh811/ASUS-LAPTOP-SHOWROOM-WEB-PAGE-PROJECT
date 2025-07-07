<!-- <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS 2025 Laptop Models</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background-color: #f8fafc;
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            color: #333;
        }

        /* Navbar Styles */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 15px 30px;
        }

        .nav-links {
            display: flex;
            gap: 25px;
        }

        .nav-links a {
            text-decoration: none;
            color: #1e3a8a;
            font-weight: 600;
            font-size: 1.1em;
            transition: color 0.3s ease;
            position: relative;
        }

        .nav-links a:hover {
            color: #f80606;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: #f80606;
            transition: width 0.3s ease;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .asus-showroom {
            padding: 120px 30px 60px;
            /* Added padding-top for navbar */
            background: linear-gradient(to right, #edf2fb, #e2eafc);
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
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

        .asus-showroom h2 {
            font-size: 3em;
            margin-bottom: 40px;
            color: #0d47a1;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
            animation: rgbColor 5s infinite;
        }

        @keyframes rgbColor {
            0% {
                color: rgb(255, 0, 0);
            }

            25% {
                color: rgb(0, 255, 0);
            }

            50% {
                color: rgb(0, 0, 255);
            }

            75% {
                color: rgb(255, 255, 0);
            }

            100% {
                color: rgb(255, 0, 255);
            }
        }

        .laptop-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            padding: 0 20px;
            margin-bottom: 40px;
        }

        .laptop-card {
            background: #fff;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.4s ease;
            border: 1px solid #dbeafe;
            overflow: hidden;
            position: relative;
            animation: rgbBorder 8s infinite;
        }

        @keyframes rgbBorder {
            0% {
                border-color: rgb(255, 0, 0);
            }

            25% {
                border-color: rgb(0, 255, 0);
            }

            50% {
                border-color: rgb(0, 0, 255);
            }

            75% {
                border-color: rgb(255, 255, 0);
            }

            100% {
                border-color: rgb(255, 0, 255);
            }
        }

        .laptop-card:hover {
            transform: scale(1.03);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
        }

        .laptop-card img {
            width: 100%;
            height: auto;
            border-radius: 12px;
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }

        .laptop-card:hover img {
            transform: scale(1.05);
        }

        .laptop-card h3 {
            font-size: 1.5em;
            color: #1e3a8a;
            margin-bottom: 15px;
        }

        .laptop-card ul {
            text-align: left;
            padding-left: 0;
            list-style: none;
        }

        .laptop-card ul li {
            font-size: 1em;
            padding: 8px 0;
            color: #555;
            border-bottom: 1px dashed #ddd;
            padding-left: 25px;
            position: relative;
        }

        .laptop-card ul li::before {
            content: '\272A';
            color: #1e40af;
            font-size: 1.2em;
            position: absolute;
            left: 0;
            top: 6px;
        }

        .back-button {
            display: inline-block;
            padding: 12px 30px;
            background-color: #f80606;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }

        .back-button:hover {
            background-color: #1e3a8a;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }

        .back-button i {
            margin-right: 8px;
        }

        @media (max-width: 768px) {
            .asus-showroom h2 {
                font-size: 2em;
            }

            .laptop-card {
                padding: 20px;
            }

            .nav-links {
                gap: 15px;
            }

            .nav-links a {
                font-size: 0.9em;
            }
        }

        @media (max-width: 480px) {
            .nav-links {
                flex-wrap: wrap;
                gap: 10px;
            }
        }
    </style>
</head>

<body>
    <!-- Navbar -->
<nav class="navbar">
    <div class="nav-links">
        <a href="./index.html">Home</a>
        <a href="./about3.html">About</a>
        <a href="./service3.html">Service</a>
        <a href="./models1.html">Laptops</a>
        <a href="./contact1.html">Contact</a>
    </div>
</nav>

<section class="asus-showroom">
    <h2>Explore the Latest ASUS 2025 Laptop Models</h2>
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
        </div>

        <!-- ROG Strix SCAR 17 -->
        <div class="laptop-card">
            <img src="./img/ROG Strix g17.jpg" alt="ROG Strix SCAR 17">
            <h3>ROG Strix SCAR 18</h3>
            <ul>
                <li>🎮 Intel Core Ultra 9 / AMD Ryzen 9</li>
                <li>💾 Up to 64GB DDR5 RAM</li>
                <li>📦 Up to 4TB PCIe Gen 4 SSD</li>
                <li>💡 AniMe Matrix™ display</li>
            </ul>
        </div>

        <!-- TUF Gaming A15 -->
        <div class="laptop-card">
            <img src="./img/asus tuf a15.jpg" alt="TUF Gaming A15">
            <h3>TUF Gaming A18</h3>
            <ul>
                <li>🧱 AMD Ryzen 7 260, RTX 5070 GPU</li>
                <li>🖥️ 16" 2.5K 165Hz display</li>
                <li>🛡️ Military-grade durability</li>
                <li>🧊 Advanced cooling system</li>
            </ul>
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
        </div>

        <!-- Zenbook S16 -->
        <div class="laptop-card">
            <img src="./img/zenbook 16.jpg" alt="ASUS Zenbook S16">
            <h3>Zenbook S16</h3>
            <ul>
                <li>💼 16" 3K OLED display</li>
                <li>🧠 AMD Ryzen AI 7 350 processor</li>
                <li>🧠 Copilot+ AI features</li>
                <li>⚡ 120Hz refresh rate</li>
            </ul>
        </div>

        <!-- Vivobook S14 -->
        <div class="laptop-card">
            <img src="./img/zenbook a14.jpg" alt="ASUS Vivobook S14">
            <h3>Vivobook S14</h3>
            <ul>
                <li>🖥️ 14" Lumina OLED display</li>
                <li>🧠 Intel Core Ultra 7 processor</li>
                <li>🔊 Harman Kardon-certified speakers</li>
                <li>🔋 75Wh battery</li>
            </ul>
        </div>

        <!-- Vivobook 14 Flip -->
        <div class="laptop-card">
            <img src="./img/vivobook 14  flip.jpg" alt="Vivobook 14 Flip">
            <h3>Vivobook 14 Flip</h3>
            <ul>
                <li>🔄 360° hinge design</li>
                <li>🖥️ 14" Lumina OLED touchscreen</li>
                <li>🧠 Intel Core Ultra 7 processor</li>
                <li>✍️ ASUS Pen 2.0 support</li>
            </ul>
        </div>

        <!-- Zenbook 14 -->
        <div class="laptop-card">
            <img src="./img/zenbook 14.jpg" alt="ASUS Zenbook 14">
            <h3>Zenbook 14</h3>
            <ul>
                <li>🖥️ 14" 3K OLED display</li>
                <li>🧠 Intel Core Ultra 9 processor</li>
                <li>💾 Up to 32GB RAM</li>
                <li>📦 Up to 1TB SSD</li>
            </ul>
        </div>

        <!-- Vivobook 16 -->
        <div class="laptop-card">
            <img src="./img/vivobook 16.jpg" alt="ASUS Vivobook 16">
            <h3>Vivobook 16</h3>
            <ul>
                <li>🖥️ 16" FHD IPS display</li>
                <li>🧠 Snapdragon X processor</li>
                <li>💾 Up to 16GB RAM</li>
                <li>🔋 Up to 17 hours battery life</li>
            </ul>
        </div>

        <!-- Gaming V16 -->
        <div class="laptop-card">
            <img src="./img/vivobookV16.jpg" alt="ASUS Gaming V16">
            <h3>Gaming V16</h3>
            <ul>
                <li>🎮 NVIDIA GeForce RTX 4050 GPU</li>
                <li>🧠 Intel Core Ultra 5 processor</li>
                <li>🖥️ 16" FHD display</li>
                <li>💾 16GB RAM, 512GB SSD</li>
            </ul>
        </div>
    </div>

    <a href="./index.html" class="back-button">
        <i class="fas fa-arrow-left"></i> Back
    </a>
</section>
</body>

</html> -->