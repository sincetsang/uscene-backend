# ============================================
# uscene-backend-main Dockerfile
# Django + uWSGI on Python 3.10
# ============================================

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files during build
RUN mkdir -p /var/uscene/static && python manage.py collectstatic --noinput

EXPOSE 8997

# uWSGI config file path
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
