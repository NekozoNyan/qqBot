FROM python:3.11-alpine3.12

WORKDIR /usr/src/app

RUN apk update && apk add --vitual build-dependencies build-base gcc && apk add tzdata

COPY requirement.txt .
RUN pip install -no-cache-dir -r requirement.txt

RUN apk del build-denpendencies

COPY . .

CMD ["hypercorn", "bot:app", "-b", "0.0.0.0:8080"]