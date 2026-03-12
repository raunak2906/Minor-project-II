# Minor-project-II

🛒 NovaMart (Orma) Full Application Walkthrough
Welcome to the comprehensive walkthrough of NovaMart (Orma). This document outlines the application's architecture, key features, signature UI/UX design, and the step-by-step user journey from landing on the homepage to completing a checkout.

1. Executive Overview
NovaMart (Orma) is a modern e-commerce web application powered by Python (Flask) on the backend and SQLite/MySQL for data persistence. The frontend is built using standard HTML, CSS, and vanilla JavaScript, leveraging Jinja2 templates for dynamic rendering.

The application aims to deliver a premium, enterprise-grade user experience characterized by high fluidity, modern aesthetics, and seamless interactions without relying on heavy frontend frameworks like React.

2. UI/UX Design Philosophy
The application interface is heavily inspired by Apple & VisionOS design systems.

Glassmorphism Engine: The main navigation header and dropdowns utilize layered CSS backdrops (backdrop-filter: blur(25px)) to create a frosted glass effect that blends dynamically with passing backgrounds.
Particle Canvas Background: A lightweight, custom-built HTML5 <canvas> particle network operates seamlessly in the background. Dots float independently, providing a sense of depth and life without distracting from products.
Curated Aesthetics: The UI features smooth padding, highly rounded corners (border-radius: 18px), soft box-shadows, and elegant typography (Poppins/Inter style).
Micro-animations: Elements respond to user input naturally. Buttons lightly scale down on click (transform: scale(0.96)), product cards zoom smoothly on hover, and pre-loaders utilize pulsing gradient animations.
3. The End-to-End User Journey
A. Landing & Onboarding
The Preloader: When launching the site, the user encounters a brief, stylized pre-loader to hide unstyled content and ensure a buttery-smooth entrance. It sets a local session flag so returning users aren't bothered by it during the same session.
The Homepage (Hero Section): A massive banner highlighting top offers alongside dynamic product showcases. Products are injected dynamically from the database using random queries for freshness.
B. Authentication Flow
Authentication uses an email-first, passwordless aesthetic:

Login Page: The user enters their email.
Smart Routing:
If the email is recognized, they are logged in directly and their user session begins.
If the email is new, the backend automatically creates a preliminary user record and immediately routes them to the Complete Profile page.
Complete Profile: The user provides their Name, Gender, and optionally uploads a Profile Picture which the app saves locally.
C. Discovery & Catalog
The Shop Page: The main catalog displays paginated/filtered products in an aesthetic CSS grid.
Intelligent Live Search:
As the user types into the search bar, the backend responds via a debounced API (/api/search).
Results instantly appear in a hovering glassmorphism dropdown mimicking Apple Spotlight, complete with product thumbnail images, titles, and routing IDs.
Voice Search Integration:
A microphone icon inside the search bar leverages the window.SpeechRecognition API.
Upon clicking, a sleek "Siri-style" overlay appears indicating listening states (Hearing sound..., Listening to speech...).
The browser physically transcribes the user's voice into text and forces an immediate search execution based on spoken intent.
D. Single Item View & Reviews
Product Detail Page: Deep dive into a specific product’s description and price point.
Review System: Authenticated users can leave star ratings and written reviews, which dynamically average out on the product's primary rating banner.
E. Add to Cart & Checkout
Cookie-Based Cart: To accommodate both logged-in and guest users, standard carts are driven by browser cookies. When a user clicks "Add to Cart", JavaScript appends the product ID to the cookie, generating a toast notification immediately.
Cart Review: The cart groups similar items together, multiplies their prices, and generates a dynamic total.
Billing Form Phase: The user provides their physical shipping address and phone number to anchor the order detail.
Mock Payment Gateway: The application generates a massive, randomized 12-digit Tracker ID. The user performs an offline/UPI payment and enters their UTR (Unique Transaction Reference) Number.
Success Page: The transaction is tied permanently to the database under 
order_detail
 and finalized with an engaging success screen.
F. User Dashboard
Users can visit their private Dashboard to view a persistent history of every previous order they've executed, including dates, tracker IDs, and total amounts.

4. Administrative Capabilities (Master Dashboard)
Admins can use the localized portal at /master to modify the storefront.

Add New Products: The product entry form allows direct insertion of new stock (name, price, detail).
Image Handling System: The Flask backend natively handles image uploads over standard HTTP forms (enctype="multipart/form-data"), automatically building structural directories (/static/img/pdimg/{Product ID}/01.jpeg) to ensure images seamlessly link to newly inserted database objects.


# NovaMart (Orma) Setup & Execution Guide

This is a step-by-step walkthrough to help you run the **NovaMart (Orma)** web application for the first time. The application is built with Flask, SQLAlchemy, and SQLite.

## 1. Prerequisites
Ensure you have Python 3 installed on your Windows machine. The project is set up with a virtual environment named `.venv`.

## 2. Activate the Virtual Environment
Open PowerShell or your preferred terminal in the project directory (`c:\Users\gaurav\Documents\Java-second-year-programs--main`) and activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```
*(If you are using Command Prompt instead, use `.\.venv\Scripts\activate.bat`)*

## 3. Install Dependencies
If you haven't installed the required Python packages yet, you need to install them. Since there is no `requirements.txt` file, you can install the necessary modules manually:

```powershell
pip install Flask Flask-SQLAlchemy Flask-Mail qrcode[pil] PyMySQL
```

## 4. Initialize the Database
The application requires a database to store products, users, orders, and reviews. There is a convenient setup script that will create the `orma.db` SQLite database and populate it with initial product data.

Run the initialization script:
```powershell
python init_sqlite.py
```
*You should see a message indicating: "Database initialized with product data for SQLite!"*

## 5. Start the Application
You currently have two main ways to run the server:

### Option A: Standard Run (Port 80)
If Port 80 is not currently in use by another service (like Apache or IIS), you can run the primary application entry point:
```powershell
python main.py
```
*Note: Depending on your system configuration, running on Port 80 might require administrative privileges.*

### Option B: Alternative Run via PyMySQL wrapper (Port 5001)
If Port 80 is blocked or you prefer to run it safely on another port, an alternative runner is provided which patches PyMySQL over MySQLdb and runs on Port 5001:
```powershell
python run_with_pymysql.py
```

## 6. Access the Application
Once the server is running, open your web browser and navigate to:
- If you used Option A: [http://localhost](http://localhost)
- If you used Option B: [http://localhost:5001](http://localhost:5001)
