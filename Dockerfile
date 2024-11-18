FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -r deepmode && useradd -r -g deepmode deepmode

WORKDIR /app

COPY requirements-docker.txt .

RUN pip3 install -r requirements-docker.txt

USER deepmode

COPY . .

VOLUME ["/app"]

CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
