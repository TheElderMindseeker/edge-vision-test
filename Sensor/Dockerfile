FROM python:3.9-slim-buster
WORKDIR /app
RUN apt update
RUN apt install -y libsdl2-dev
RUN apt clean
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY sensor sensor
CMD ["python", "-m", "sensor"]
