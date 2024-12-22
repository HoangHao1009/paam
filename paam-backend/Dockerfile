FROM python:3.13.1

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
