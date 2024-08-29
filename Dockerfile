FROM python:3.9
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY /product .
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh"]
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]