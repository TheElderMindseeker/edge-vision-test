FROM python:3.9-slim-buster
WORKDIR /app
COPY sensor sensor
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install -y libsdl2-dev
RUN apt clean
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "-m", "sensor"]
