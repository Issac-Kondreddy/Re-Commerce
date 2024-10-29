# Start from an official Python image
FROM python:3.11-slim

# Set environment variables to ensure the container runs properly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Run collectstatic to gather static files (assumes settings.py has proper STATIC_ROOT defined)
RUN python manage.py collectstatic --noinput

# Expose the port the application will run on
EXPOSE 8000

# Use gunicorn as the WSGI server to serve the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "user_service.wsgi:application"]
