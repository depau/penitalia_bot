FROM python:3.11-alpine
RUN apk add --no-cache ffmpeg
COPY setup.py /app/
COPY penitaliabot /app/penitaliabot
WORKDIR /app
RUN pip install -e .
ENTRYPOINT ["penitaliabot"]
