# orbital-bookstore
Bookstore for casual readers


Orbital Bookstore is a web-based e-commerce platform for buying books and e-books. Users can browse books, e-books, and accessories, add them to their cart or favorites, leave reviews, and place orders. The application also features an interactive image carousel on the homepage, a weather widget, and more.

Features

Browse physical books, e-books, and various accessories
Add items to the cart or favorites list
View book and e-book details
User authentication (login, registration)
Dynamic search functionality
Interactive carousel for book and e-book covers
Weather widget displaying real-time weather information
Order placement with delivery options for physical products or downloadable e-books
Review system for books and e-books
Responsive layout with Flexbox design

Installation

Prerequisites

Python 3.8 or higher
Django 5.1
MySQL database
Git (for version control)
A virtual environment (recommended)
Step-by-Step Installation

Clone the repository


git clone https://github.com/yourusername/orbital-bookstore.git
cd orbital-bookstore

Set up a virtual environment

Create a virtual environment and activate it:

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies

Install the necessary Python packages using pip:


pip install -r requirements.txt
Set up the MySQL database

Create a new MySQL database and update the settings.py with your database credentials.

Run migrations

After configuring the database, run the following command to apply migrations and set up your database tables:


python manage.py migrate

Create a superuser

To access the admin panel and manage the content:


python manage.py createsuperuser

Run the development server

Start the server:


python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

Usage

Homepage
The homepage features a search bar, book carousel, and weather widget. Use the search bar to find books or e-books by title or author. Hover over the carousel to browse book and e-book covers, or click on a cover to view its details.

Product Pages

Browse books, e-books, and accessories using the navigation bar.
Add items to your cart or favorites list.
View detailed information on book or e-book product pages.
Order Placement
Once you've added items to your cart, you can proceed to "checkout", choose a delivery option, and place an order.

Reviews

Leave reviews for books and e-books you've purchased.

Admin Panel

Access the admin panel at /admin to manage products, categories, and user orders.



## Demo Video

[Click here to watch the demo video](https://github.com/ott4444/orbital-bookstore/blob/main/preview.mp4)