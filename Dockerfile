FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./app/wsgi.py", "0.0.0.0:5000" ]