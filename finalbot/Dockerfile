FROM python:3

COPY . /app

WORKDIR /app/

ENV PYTHONPATH /app/console_bot

RUN python setup.py install

CMD ["console-bot"]