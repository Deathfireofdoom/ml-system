FROM python:3.11-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src

CMD ["gunicorn", "-b", "0.0.0.0:5050", "run:flask_app"]
