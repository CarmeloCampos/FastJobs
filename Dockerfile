FROM python:3.12.2-alpine

ENV TZ="America/Los_Angeles"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "bot.py" ]