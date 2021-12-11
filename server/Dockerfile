FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /server
WORKDIR /server
COPY requirements.txt /server/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /server/ 
RUN python manage.py collectstatic --noinput
EXPOSE 8000