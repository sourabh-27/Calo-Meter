# pull official base image
FROM 779152395358.dkr.ecr.ap-south-1.amazonaws.com/python:3.8-newrelic

# copy newrelic config
COPY newrelic.ini /caloriemeter/newrelic.ini

#set timezone to india/kolkata
RUN apt-get install -yyq tzdata && \
    cp /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" >  /etc/timezone

# set work directory
WORKDIR /caloriemeter

# copy the files
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .
EXPOSE 9001
# Command to execute
#CMD gunicorn --bind 0.0.0.0:9001 main:app -w 4 -k uvicorn.workers.UvicornWorker --reload --access-logfile - --error-logfile - --log-level info
CMD ["gunicorn", "-b :9001", "main:app", "-w 4", "-k uvicorn.workers.UvicornWorker"]