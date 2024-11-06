# api_gateway/Dockerfile
FROM nginx:latest

# Copy NGINX config
COPY nginx.conf /etc/nginx/nginx.conf

# Install FastAPI dependencies for background service
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --break-system-packages fastapi httpx uvicorn


# Copy FastAPI app
COPY main.py /app/main.py

# Run FastAPI in the background
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'
