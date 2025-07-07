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
    <title>ASUS Showroom Admin - Inventory</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-gray: #333333;
            --asus-light: #f5f5f5;
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;
            --sidebar-width: 250px;
            --sidebar-collapsed-width: 70px;
            --transition-speed: 0.3s;
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
            background-color: #f9f9f9;
            overflow-x: hidden;
        }

        /* Vertical Navbar with Enhanced ASUS Theme */
        .sidebar {
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }

        .sidebar-header {
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transition: all var(--transition-speed) ease;
            background: rgba(255, 0, 0, 0.1);
        }

        .sidebar-header img {
            width: 40px;
            margin-right: 10px;
            transition: all var(--transition-speed) ease;
        }

        .sidebar-header h3 {
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all var(--transition-speed) ease;
        }

        .sidebar-header span {
            color: var(--asus-red);
            font-weight: 700;
        }

        .nav-menu {
            padding: 20px 0;
        }

        .nav-item {
            position: relative;
            margin: 5px 0;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
            position: relative;
            overflow: hidden;
            font-weight: 500;
        }

        .nav-link i {
            margin-right: 15px;
            font-size: 1.1rem;
            color: var(--asus-red);
            transition: all var(--transition-speed) ease;
            min-width: 20px;
        }

        .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
            transform: translateX(5px);
        }

        .nav-link:hover i {
            transform: scale(1.2);
            color: white;
        }

        .nav-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--asus-red);
            transform: scaleY(0);
            transform-origin: center;
            transition: transform var(--transition-speed) ease;
        }

        .nav-link:hover::before {
            transform: scaleY(1);
        }

        .nav-link.active {
            background: rgba(255, 0, 0, 0.2);
            padding-left: 25px;
        }

        .nav-link.active i {
            color: white;
            transform: scale(1.1);
        }

        .nav-link.active::before {
            transform: scaleY(1);
        }

        .dropdown-menu {
            padding-left: 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--transition-speed) ease;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 0 0 8px 8px;
        }

        .dropdown-menu.show {
            max-height: 300px;
            animation: dropdownOpen 0.4s ease forwards;
        }

        @keyframes dropdownOpen {
            0% {
                opacity: 0;
                transform: translateY(-10px);
            }

            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .dropdown-menu .nav-link {
            padding: 10px 20px 10px 45px;
            font-size: 0.9rem;
            background: transparent;
        }

        .dropdown-menu .nav-link:hover {
            background: rgba(255, 0, 0, 0.1);
        }

        .dropdown-toggle {
            cursor: pointer;
        }

        .dropdown-toggle::after {
            content: '\f078';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 20px;
            transition: all var(--transition-speed) ease;
        }

        .dropdown-toggle.active::after {
            transform: rotate(180deg);
            color: white;
        }

        .logout {
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }

        .logout .nav-link {
            color: var(--asus-red);
        }

        .logout .nav-link i {
            color: var(--asus-red);
        }

        .logout .nav-link:hover {
            background: rgba(255, 0, 0, 0.15);
            color: white;
        }

        .logout .nav-link:hover i {
            color: white;
        }

        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            width: calc(100% - var(--sidebar-width));
            padding: 30px;
            transition: all var(--transition-speed) ease;
        }

        /* Inventory Styles */
        .inventory-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            padding: 30px;
            animation: fadeIn 0.6s ease;
        }

        .inventory-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .inventory-header h2 {
            color: var(--asus-black);
            font-size: 1.8rem;
        }

        .inventory-header h2 i {
            color: var(--asus-red);
            margin-right: 10px;
        }

        .btn-add {
            background: var(--asus-red);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
        }

        .btn-add:hover {
            background: #cc0000;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
        }

        .btn-add i {
            margin-right: 8px;
        }

        .inventory-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .inventory-table th,
        .inventory-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .inventory-table th {
            background: var(--asus-black);
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
        }

        .inventory-table tr:hover {
            background-color: rgba(255, 0, 0, 0.03);
        }

        .product-image {
            width: 60px;
            height: 60px;
            object-fit: contain;
            border-radius: 5px;
            background: #f5f5f5;
            padding: 5px;
            border: 1px solid #eee;
        }

        .status-in-stock {
            background: rgba(76, 175, 80, 0.15);
            color: var(--positive);
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: 600;
            display: inline-block;
        }

        .status-low-stock {
            background: rgba(255, 152, 0, 0.15);
            color: var(--warning);
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: 600;
            display: inline-block;
        }

        .status-out-of-stock {
            background: rgba(244, 67, 54, 0.15);
            color: var(--negative);
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: 600;
            display: inline-block;
        }

        .action-buttons {
            display: flex;
            gap: 8px;
        }

        .btn-action {
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            display: flex;
            align-items: center;
        }

        .btn-action i {
            margin-right: 5px;
        }

        .btn-edit {
            background: rgba(33, 150, 243, 0.15);
            color: var(--info);
            border: 1px solid var(--info);
        }

        .btn-edit:hover {
            background: var(--info);
            color: white;
        }

        .btn-delete {
            background: rgba(244, 67, 54, 0.15);
            color: var(--negative);
            border: 1px solid var(--negative);
        }

        .btn-delete:hover {
            background: var(--negative);
            color: white;
        }

        .btn-view {
            background: rgba(0, 150, 136, 0.15);
            color: #009688;
            border: 1px solid #009688;
        }

        .btn-view:hover {
            background: #009688;
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

        /* Responsive adjustments */
        @media (max-width: 992px) {
            .sidebar {
                width: var(--sidebar-collapsed-width);
                overflow: hidden;
            }

            .sidebar-header h3,
            .nav-link span,
            .dropdown-toggle::after {
                opacity: 0;
                display: none;
            }

            .sidebar-header {
                justify-content: center;
                padding: 20px 10px;
            }

            .sidebar-header img {
                margin-right: 0;
            }

            .nav-link {
                justify-content: center;
                padding: 12px 10px;
            }

            .nav-link i {
                margin-right: 0;
                font-size: 1.3rem;
            }

            .main-content {
                margin-left: var(--sidebar-collapsed-width);
                width: calc(100% - var(--sidebar-collapsed-width));
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
                <a href="adm-dashboard2.html" class="nav-link">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </div>

            <div class="nav-item">
                <div class="nav-link dropdown-toggle">
                    <i class="fas fa-users"></i>
                    <span>Employees</span>
                </div>
                <div class="dropdown-menu">
                    <div class="nav-item">
                        <a href="adm-emp-addform.html" class="nav-link">
                            <i class="fas fa-user-plus"></i>
                            <span>Add Employee</span>
                        </a>
                    </div>
                    <div class="nav-item">
                        <a href="employee-list.html" class="nav-link">
                            <i class="fas fa-list"></i>
                            <span>Employee List</span>
                        </a>
                    </div>
                </div>
            </div>

            <div class="nav-item">
                <a href="leave-requests.html" class="nav-link">
                    <i class="fas fa-calendar-minus"></i>
                    <span>Leave Requests</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="salary.html" class="nav-link">
                    <i class="fas fa-money-bill-wave"></i>
                    <span>Salary</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="inv.html" class="nav-link active">
                    <i class="fas fa-laptop"></i>
                    <span>Inventory</span>
                </a>
            </div>

            <div class="nav-item">
                <a href="orders.html" class="nav-link">
                    <i class="fas fa-shopping-cart"></i>
                    <span>Orders</span>
                </a>
            </div>

            <div class="nav-item logout">
                <a href="login1.html" class="nav-link">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Logout</span>
                </a>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <div class="inventory-container">
            <div class="inventory-header">
                <h2><i class="fas fa-laptop"></i> ASUS Laptop Inventory</h2>
                <button class="btn-add" onclick="openAddProductModal()">
                    <i class="fas fa-plus"></i> Add Product
                </button>
            </div>

            <table class="inventory-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Product Name</th>
                        <th>Model</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- ASUS ROG Zephyrus G14 -->
                    <tr>
                        <td><img src="https://dlcdnwebimgs.asus.com/gain/4E6A9D4C-1E4F-4A0B-8F2C-9A5F1B3F1A13"
                                alt="ROG Zephyrus G14" class="product-image"></td>
                        <td>ROG Zephyrus G14</td>
                        <td>GA401QM</td>
                        <td>Gaming</td>
                        <td>$1,499.99</td>
                        <td>25</td>
                        <td><span class="status-in-stock">In Stock</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-action btn-edit"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-action btn-view"><i class="fas fa-eye"></i> View</button>
                            </div>
                        </td>
                    </tr>

                    <!-- ASUS ZenBook 14 -->
                    <tr>
                        <td><img src="https://dlcdnwebimgs.asus.com/gain/4E6A9D4C-1E4F-4A0B-8F2C-9A5F1B3F1A13"
                                alt="ZenBook 14" class="product-image"></td>
                        <td>ZenBook 14</td>
                        <td>UX425EA</td>
                        <td>Ultrabook</td>
                        <td>$999.99</td>
                        <td>12</td>
                        <td><span class="status-in-stock">In Stock</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-action btn-edit"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-action btn-view"><i class="fas fa-eye"></i> View</button>
                            </div>
                        </td>
                    </tr>

                    <!-- ASUS TUF Gaming F15 -->
                    <tr>
                        <td><img src="https://dlcdnwebimgs.asus.com/gain/4E6A9D4C-1E4F-4A0B-8F2C-9A5F1B3F1A13"
                                alt="TUF Gaming F15" class="product-image"></td>
                        <td>TUF Gaming F15</td>
                        <td>FX506HM</td>
                        <td>Gaming</td>
                        <td>$1,199.99</td>
                        <td>5</td>
                        <td><span class="status-low-stock">Low Stock</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-action btn-edit"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-action btn-view"><i class="fas fa-eye"></i> View</button>
                            </div>
                        </td>
                    </tr>

                    <!-- ASUS VivoBook S15 -->
                    <tr>
                        <td><img src="https://dlcdnwebimgs.asus.com/gain/4E6A9D4C-1E4F-4A0B-8F2C-9A5F1B3F1A13"
                                alt="VivoBook S15" class="product-image"></td>
                        <td>VivoBook S15</td>
                        <td>S533EA</td>
                        <td>Everyday</td>
                        <td>$799.99</td>
                        <td>0</td>
                        <td><span class="status-out-of-stock">Out of Stock</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-action btn-edit"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-action btn-view"><i class="fas fa-eye"></i> View</button>
                            </div>
                        </td>
                    </tr>

                    <!-- ASUS ExpertBook B9 -->
                    <tr>
                        <td><img src="https://dlcdnwebimgs.asus.com/gain/4E6A9D4C-1E4F-4A0B-8F2C-9A5F1B3F1A13"
                                alt="ExpertBook B9" class="product-image"></td>
                        <td>ExpertBook B9</td>
                        <td>B9450FA</td>
                        <td>Business</td>
                        <td>$1,599.99</td>
                        <td>15</td>
                        <td><span class="status-in-stock">In Stock</span></td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn-action btn-edit"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-action btn-view"><i class="fas fa-eye"></i> View</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Dropdown functionality
        document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
            toggle.addEventListener('click', function () {
                this.classList.toggle('active');
                const menu = this.nextElementSibling;
                menu.classList.toggle('show');

                // Close other dropdowns when opening a new one
                document.querySelectorAll('.dropdown-toggle').forEach(otherToggle => {
                    if (otherToggle !== this) {
                        otherToggle.classList.remove('active');
                        otherToggle.nextElementSibling.classList.remove('show');
                    }
                });
            });
        });

        // Function to open add product modal (placeholder)
        function openAddProductModal() {
            alert("Add Product form would open here in a real implementation");
            // In a real implementation, this would open a modal with a form to add new products
        }

        // Make table rows clickable (for view functionality)
        document.querySelectorAll('.inventory-table tbody tr').forEach(row => {
            row.addEventListener('click', function (e) {
                // Don't trigger if clicking on action buttons
                if (!e.target.closest('.btn-action')) {
                    alert("View details for: " + this.querySelector('td:nth-child(2)').textContent);
                    // In a real implementation, this would open a detailed view or modal
                }
            });
        });
    </script>
</body>

</html>
      """)