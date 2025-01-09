FROM python:3.12-alpine 

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    g++ \
    make \
    zlib-dev \
    bash \
    postgresql-dev \
    libpq

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /uploads

# Cấp quyền cho thư mục
RUN chmod -R 777 /uploads

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
