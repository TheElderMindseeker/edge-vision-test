FROM python:3.9-slim-buster
WORKDIR /app
COPY controller controller
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8087
CMD ["python", "-m", "controller"]
