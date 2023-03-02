FROM python:3.8-slim-buster
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod 775 start.sh
CMD "./start.sh"
