FROM python:3.8-buster

RUN apt-get update && apt-get install -y git git-core && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /
RUN python -m pip install -r /requirements.txt
WORKDIR /app
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["rq"]
