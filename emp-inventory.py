#!C:/Python/python.exe
import sys
import io
import os
import cgi
import cgitb
import pymysql

# Enable CGI traceback
cgitb.enable()

# Set UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("Content-type:text/html\r\n\r\n")

form = cgi.FieldStorage()
pid = form.getvalue("id")
message = ""

# Handle form submission
if os.environ['REQUEST_METHOD'] == 'POST':
    try:
        category = form.getvalue("category")
        model = form.getvalue("model")
        series = form.getvalue("series")
        processor = form.getvalue("processor")
        gpu = form.getvalue("gpu")
        ram = form.getvalue("ram")
        storage = form.getvalue("storage")
        price = form.getvalue("price")
        quantity = form.getvalue("quantity")
        features = form.getvalue("features")

        # Connect to MySQL
        con = pymysql.connect(host="localhost", user="root", password="", database="final_laptopproject")
        cur = con.cursor()

        # Insert data into the inventory table
        query = """
            INSERT INTO `emp_inv_addform`
            (Category, Laptop_model, Series, Processor, Graphics_Card, RAM, Storage, Price, Quantity, Additional_features, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(query, (category, model, series, processor, gpu, ram, storage, price, quantity, features, 'pending'))

        con.commit()
        message = "<script>alert('Laptop added successfully!'); window.location.href='emp-inventory.py?id=%s';</script>" % pid

    except pymysql.Error as e:
        message = f"<h3 style='color:red;'>Database Error: {e}</h3>"

    finally:
        if 'con' in locals() and con:
            con.close()

# HTML starts here
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASUS Inventory - Add Laptop</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');

        :root {{
            --asus-black: #000000;
            --asus-red: #FF0000;
            --asus-gray: #333333;
            --asus-light: #f5f5f5;
            --positive: #4CAF50;
            --negative: #F44336;
            --warning: #FF9800;
            --info: #2196F3;
            --sidebar-width: 250px;
            --transition-speed: 0.3s;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }}

        body {{
            display: flex;
            min-height: 100vh;
            background-color: #f9f9f9;
            overflow-x: hidden;
        }}

        /* Sidebar */
        .sidebar {{
            width: var(--sidebar-width);
            background: var(--asus-black);
            color: white;
            height: 100vh;
            position: fixed;
            transition: all var(--transition-speed) ease;
            z-index: 1000;
            background-image: linear-gradient(to bottom, #000000, #1a1a1a);
        }}

        .sidebar-header {{
            padding: 20px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 0, 0, 0.1);
        }}

        .sidebar-header img {{
            width: 40px;
            margin-right: 10px;
        }}

        .sidebar-header h3 {{
            font-size: 1.2rem;
            color: white;
            font-weight: 700;
        }}

        .sidebar-header span {{
            color: var(--asus-red);
            font-weight: 700;
        }}

        .nav-menu {{
            padding: 20px 0;
        }}

        .nav-item {{
            margin: 5px 0;
        }}

        .nav-link {{
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
            position: relative;
            overflow: hidden;
            font-weight: 500;
        }}

        .nav-link i {{
            margin-right: 15px;
            font-size: 1.1rem;
            color: var(--asus-red);
            transition: all var(--transition-speed) ease;
        }}

        .nav-link:hover {{
            background: rgba(255, 0, 0, 0.15);
            padding-left: 25px;
            transform: translateX(5px);
        }}

        .dropdown-menu {{
            padding-left: 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--transition-speed) ease;
            background: rgba(0, 0, 0, 0.2);
        }}

        .dropdown-menu.show {{
            max-height: 300px;
        }}

        .dropdown-menu a {{
            display: block;
            padding: 10px 15px;
            color: white;
            text-decoration: none;
            transition: all var(--transition-speed) ease;
        }}

        .dropdown-menu a:hover {{
            background: rgba(255, 0, 0, 0.2);
            padding-left: 20px;
        }}

        .logout {{
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }}

        .main-content {{
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 25px;
            transition: all var(--transition-speed);
        }}

        /* Form Styles */
        .form-container {{
            max-width: 700px;
            margin: 20px auto;
            padding: 30px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        h2 {{
            text-align: center;
            color: var(--asus-gray);
            margin-bottom: 20px;
        }}

        .form-group {{
            margin-bottom: 20px;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }}

        input, select, textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}

        input:focus, select:focus, textarea:focus {{
            border-color: var(--asus-red);
            outline: none;
        }}

        textarea {{
            min-height: 100px;
            resize: vertical;
        }}

        button {{
            background-color: var(--asus-red);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s;
            display: block;
            margin: 30px auto 0;
            font-weight: 600;
        }}

        button:hover {{
            background-color: #cc0000;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                flex-direction: column;
            }}

            .sidebar {{
                width: 70px;
            }}

            .sidebar-header h3,
            .nav-link span {{
                display: none;
            }}

            .nav-link {{
                justify-content: center;
                padding: 15px 0;
            }}

            .main-content {{
                margin-left: 70px;
            }}
        }}
    </style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
    <div class="sidebar-header">
        <img src="./img/asus-republic-of-gamers-seeklogo.png" alt="ASUS Logo">
       <h3>EMPLOYEE <span>DASHBOARD</span></h3>
    </div>
    <ul class="nav-menu">
        <li class="nav-item">
            <a href="emp1-dash.py?id={pid}" class="nav-link">
                <i class="fas fa-tachometer-alt"></i>
                <span>Dashboard</span>
            </a>
        </li>
       
        <li class="nav-item">
            <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                <i class="fas fa-laptop"></i>
                <span>Inventory ▼</span>
            </div>
            <ul class="dropdown-menu">
                <li><a href="emp-inventory.py?id={pid}">Add Laptop</a></li>
                <li><a href="emp-inv-tableview.py?id={pid}">Inventory List</a></li>
            </ul>
        </li>
        <li class="nav-item">
            <div class="nav-link dropdown-toggle" onclick="toggleDropdown(this)">
                <i class="fas fa-calendar-minus"></i>
                <span>Leave Request ▼</span>
            </div>
            <ul class="dropdown-menu">
                <li><a href="emp-leave.py?id={pid}">Request Form</a></li>
                <li><a href="emp-leavehis.py?id={pid}">History</a></li>
            </ul>
        </li>
          <li class="nav-item">
            <a href="emp-salary-view.py?id={pid}" class="nav-link">
                <i class="fas fa-money-bill-wave"></i>
                <span>salary view</span>
            </a>
        </li>
        <li class="nav-item logout">
            <a href="employee_login.py" class="nav-link">
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            </a>
        </li>
    </ul>
</div>

<!-- Main Content -->
<div class="main-content">
    <div class="form-container">
        <h2>Add New Laptop to Inventory</h2>
        {message}
        <form method="post" action="emp-inventory.py?id={pid}">
            <div class="form-group">
                <label for="category">Category</label>
                <select id="category" name="category" required>
                    <option value="">Select Category</option>
                    <option value="ROG">Republic of Gamers (ROG)</option>
                    <option value="TUF">TUF Gaming</option>
                    <option value="ZenBook">ZenBook</option>
                    <option value="VivoBook">VivoBook</option>
                    <option value="ProArt">ProArt StudioBook</option>
                    <option value="ExpertBook">ExpertBook</option>
                </select>
            </div>
            <div class="form-group">
                <label for="model">Laptop Model</label>
                <input type="text" id="model" name="model" required>
            </div>
            <div class="form-group">
                <label for="series">Series</label>
                <input type="text" id="series" name="series" required>
            </div>
            <div class="form-group">
                <label for="processor">Processor</label>
                <input type="text" id="processor" name="processor" required>
            </div>
            <div class="form-group">
                <label for="gpu">Graphics Card</label>
                <input type="text" id="gpu" name="gpu" required>
            </div>
            <div class="form-group">
                <label for="ram">RAM</label>
                <input type="text" id="ram" name="ram" required>
            </div>
            <div class="form-group">
                <label for="storage">Storage</label>
                <input type="text" id="storage" name="storage" required>
            </div>
            <div class="form-group">
                <label for="price">Price (INR)</label>
                <input type="number" id="price" name="price" required>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity</label>
                <input type="number" id="quantity" name="quantity" min="1" required>
            </div>
            <div class="form-group">
                <label for="features">Additional Features</label>
                <textarea id="features" name="features" rows="4"></textarea>
            </div>
            <button type="submit">Add Laptop</button>
        </form>
    </div>
</div>

<script>
    // Dropdown toggle
    function toggleDropdown(el) {{
        el.classList.toggle("active");
        const menu = el.nextElementSibling;
        menu.classList.toggle("show");
    }}

    // Responsive sidebar toggle
    function toggleSidebar() {{
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('collapsed');
    }}
</script>

</body>
</html>
""")