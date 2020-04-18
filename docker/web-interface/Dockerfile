FROM python:3.8-buster

COPY requirements.txt /
RUN python -m pip install -r /requirements.txt
WORKDIR /app
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["mam"]
