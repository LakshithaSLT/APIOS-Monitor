# # FROM python:latest
# FROM alpine:latest
# LABEL Maintainer="sltthenuwara@gmail.com"


# WORKDIR /usr/app/src
# # # EXPOSE 3308/tcp

# # # COPY /publish_temp.py ./
# # COPY /publish_oil.py ./
# # COPY /subscribe.py ./

# RUN apk update
# RUN apk add python3 py3-pip
# RUN apk add flask
# # RUN apk add python3 py3-pip
# # RUN apk add wget
# # RUN pip install --upgrade pip
# # RUN pip install paho-mqtt
# # RUN pip install mysql-connector-python
# # RUN mkdir /app


# # CMD [ "python", "./publish_temp.py"]
# # CMD [ "python", "./publish_oil.py"]
# # CMD [ "python", "./subscribe.py"]
# CMD [ "python", "./flask.py"]

#---------------------- Mortor Speed -----------------------------------#
# FROM alpine:latest
# LABEL Maintainer="sltthenuwara@gmail.com"

# WORKDIR /usr/app/src

# COPY /subscribe.py ./

# RUN apk update
# RUN apk add python3 py3-pip
# RUN pip install --upgrade pip
# RUN pip install paho-mqtt
# RUN pip install mysql-connector-python

# CMD [ "python", "./subscribe.py"]

# docker image build -t sltuwe_sub:0.0.10 /Users/lakshitha/Desktop/sewing/Apios

#----------------------  Mortor Speed END-----------------------------------#

#---------------------- Email Trigger -----------------------------------#
FROM alpine 
LABEL Maintainer="sltthenuwara@gmail.com"

WORKDIR /usr/app/src

COPY /email_trigger.py ./

# RUN apk update
# RUN apk add python3 py3-pip
RUN pip install --upgrade pip
RUN pip install secure-smtplib

RUN pip install mysql-connector-python

# CMD [ "python", "./email_trigger.py"]

# docker image build -t sltuwe_email:0.0.10 /Users/lakshitha/Desktop/sewing/Apios/

#----------------------  Email Trigger END-----------------------------------#

# #---------------------- Mortor Speed -----------------------------------#
# FROM alpine:latest
# LABEL Maintainer="sltthenuwara@gmail.com"

# # WORKDIR /usr/app/src

# COPY /motor_speed.py ./

# RUN apk update
# RUN apk add python3 py3-pip
# RUN pip install --upgrade pip
# RUN pip install paho-mqtt

# CMD [ "python", "./motor_speed.py"]

# # docker image build -t sltuwe_motor:0.0.10 /Users/lakshitha/Desktop/sewing/Apios

# #----------------------  Mortor Speed END-----------------------------------#



# docker image build -t sltuwe_temp:0.0.10 /Users/lakshitha/Desktop/sewing/Apios

# docker image build -t sltuwe_oil:0.0.10 /Users/lakshitha/Desktop/sewing/Apios

# docker image build -t sltuwe_sub:0.0.10 /Users/lakshitha/Desktop/sewing/Apios

# docker image build -t uwe_flask:0.0.10 /Users/lakshitha/Desktop/sewing/Apios
