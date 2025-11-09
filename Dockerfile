# ==============================
# 1️⃣ Base image
# ==============================
FROM python:3.12-slim
# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Set working directory
WORKDIR /usr/src/app

# ==============================
# 2️⃣ Install dependencies
# ==============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .
# ==============================
# 4️⃣ Run migrations + start server
# ==============================
# Run migrations when container starts
CMD ["sh", "-c", "python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"]

# Expose Django port
EXPOSE 8000
