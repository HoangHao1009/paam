FROM python:3.10-alpine 

RUN apk add --no-cache gcc musl-dev libffi-dev g++ make zlib-dev bash

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
