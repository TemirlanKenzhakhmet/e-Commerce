# E-commerce Website
This repository contains the code for an E-commerce website built using the Django framework. The website incorporates various tools and technologies, including HTMX, Tailwind CSS, RabbitMQ, and a REST API powered by RabbitMQ, to enhance the user experience and functionality.

## Features
- User Registration and Authentication: Users can sign up and log in to the website to access personalized features such as adding items to their cart, making purchases.
- Product Catalog: The website provides a comprehensive product catalog with categories and search functionality. Users can browse through the products, view detailed descriptions, and add items to their cart.
- Shopping Cart: Users can add products to their shopping cart and manage the quantity of each item. The cart allows users to review their selected items before proceeding to the checkout process.
- Secure Checkout: The website implements a secure checkout process that includes capturing shipping and billing information. Users can review their order details and make secure payments using various payment gateways. (TODO)
- Order Tracking: After completing a purchase, users can track their order status and receive updates on the progress of their shipment. (TODO)
- User Reviews and Ratings: Users can leave reviews and ratings for products they have purchased, providing valuable feedback to other users. (TODO)
- Admin Panel: The website includes an admin panel that allows administrators to manage products, orders, customers, and other aspects of the e-commerce platform.
- REST API with RabbitMQ: The website provides a RESTful API for external services to interact with the e-commerce platform. RabbitMQ is used as a message broker to handle communication and asynchronous processing of API requests.

## Technologies Used
- Django: A powerful Python web framework used for building the website's backend structure and handling user interactions.
- HTMX: A lightweight JavaScript library that allows for seamless and dynamic web page updates without the need for full-page reloads.
- Tailwind CSS: A utility-first CSS framework used for styling the website, providing a modern and responsive design.
- RabbitMQ: A message broker that enables asynchronous communication and event-driven architecture. It is used for handling API requests and processing tasks in the background.
- REST API: The website provides a RESTful API for external services to interact with the e-commerce platform. RabbitMQ is utilized to handle the communication and processing of API requests.

## Installation
To set up and run the E-commerce website locally, follow these steps:

1. Clone the repository to your local machine.
```bash
git clone https://github.com/TemirlanKenzhakhmet/TryDjango.git
```
2. Install the required dependencies using pip. For more information on installing RabbitMQ on Windows, please visit [www.rabbitmq.com](https://www.rabbitmq.com/#getstarted).
```bash
pip install -r requirements.txt
```
3. Set up the database by running database migrations.
```bash
python manage.py migrate
```
4. Start the development server.
```bash
python manage.py runserver
```
5. Access the website in your browser by visiting **http://localhost:8000**.

## Configuration
The E-commerce website can be further configured to suit specific requirements:
- Database Configuration: By default, the website uses SQLite as the database backend. For production use, it is recommended to configure a more robust database such as PostgreSQL or MySQL.
- Static Files and Media: The project utilizes Django's static and media handling capabilities. Ensure that the appropriate storage backends are configured for static files and media uploads.
- Payment Gateway Integration: The website currently does not supports any payment gateways.
- RabbitMQ Configuration: Set up RabbitMQ with appropriate credentials and configure the project to use the RabbitMQ.




