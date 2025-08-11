🚀 RevenueRadar
RevenueRadar is a sleek, interactive sales dashboard designed to empower businesses with clear, actionable insights. Monitor your revenue, spot trends, and analyze your sales performance effortlessly — all through a secure, user-friendly web app with powerful visualizations and personalized features.

✨ Key Features
🔐 Secure User Authentication
Register and log in with email verification via OTP to keep your data safe.

🎨 Light & Dark Mode
Switch themes instantly for comfortable viewing anytime.

🔍 Dynamic Data Filters
Slice and dice sales data by date, region, and category for tailored insights.

📊 Insightful Visualizations

Top products by revenue (Bar Chart)

Monthly revenue trends (Line Chart)

Revenue distribution by category (Pie Chart)

📈 Real-Time KPIs
Track total revenue, quantity sold, and average order value at a glance.

📋 Interactive Data Table
Explore filtered sales data in an intuitive, sortable table.

🛡️ Strong Password Enforcement
Secure your account with robust password criteria during signup.

🛠️ Installation & Setup
Clone the repo:

bash
Copy
Edit
git clone https://github.com/yourusername/RevenueRadar.git
cd RevenueRadar
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
streamlit run dashboard.py
📋 Usage Guide
Create a new account with a unique username and valid email address.

Verify your email with the OTP provided during registration (displayed for demo).

Log in securely and explore your personalized sales dashboard.

Use the sidebar to filter data and switch between light/dark modes.

Dive into KPIs and charts to understand your sales performance deeply.

🧰 Technologies Used
Python 3.8+

Streamlit – Lightning-fast UI for data apps

Pandas – Data analysis and manipulation

Plotly Express – Interactive and beautiful charts

JSON – Lightweight user data storage

📊 Data Requirements
Place a CSV file named salesdata.csv in the root folder. It should contain:

Column	Description
Date	Sales date (YYYY-MM-DD format)
Region	Sales region
Category	Product category
Product	Product name
Quantity	Units sold
Revenue	Revenue amount (₹)

Ensure the data is clean for best results!

🚀 Roadmap & Future Features
✅ Email service integration for real OTP delivery

🔒 Role-based access control

📄 Export reports to PDF/Excel

🤖 Advanced analytics with ML models

🔐 OAuth and multi-factor authentication for enhanced security

📄 License
Released under the MIT License. See LICENSE for details.
