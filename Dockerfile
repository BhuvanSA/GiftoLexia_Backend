FROM python:3.11-alpine

# Install build dependencies
# RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Remove build dependencies
# RUN apk del .build-deps
EXPOSE 8081
EXPOSE 8082
EXPOSE 8085

CMD [ "python", "app.py"]