FROM python:3.9

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python3 main.py