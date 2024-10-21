# ReCommerce

ReCommerce is a microservices-based e-commerce platform focused on **recommendation learning**. It leverages machine learning to provide personalized product recommendations and is designed for scalability and performance. **Note:** This project is still in progress.

## Core Services
1. **User Service** – Handles user authentication, registration, and profile management.
2. **Order Service** – Manages order creation, tracking, and history.
3. **Product Service** – Manages product catalog, inventory, and pricing.
4. **Recommendation Service** – Provides personalized product recommendations using machine learning.
5. **Notification Service** – Sends notifications via email or SMS for order confirmations, updates, etc.

## Tech Stack

### Frontend:
- HTML
- CSS
- JavaScript (Optional, since it's primarily backend-focused)

### Backend:
- Python
- Django (Django Rest Framework for APIs)

### Databases:
- PostgreSQL (For relational data: users, orders)
- MongoDB (For flexible, unstructured product data)

### Communication between Microservices:
- **API Gateway**: NGINX for routing traffic to microservices.

### Containerization:
- **Docker** for containerizing services.
- **Docker Compose** for local development and orchestrating containers.

### Deployment:
- **AWS** (EC2, RDS, S3) for cloud deployment and scaling.

### Asynchronous Tasks:
- **Celery** + **Redis** for handling background tasks (e.g., sending notifications).

### Message Queue:
- **RabbitMQ** for managing inter-service communication and queuing tasks.

### Machine Learning:
- Used in the **Recommendation Service** to provide personalized product recommendations based on user behavior and product interactions.

### Search:
- **Elasticsearch** for fast, full-text product search capabilities.

---

## Project Status:
This project is currently **in progress**. Further updates and additional features will be implemented in upcoming phases.
