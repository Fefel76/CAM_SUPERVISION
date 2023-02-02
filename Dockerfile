FROM mypython

#FROM python:3.8.16-slim
#ENV TZ="Europe/Paris"
#RUN apt-get update && apt install -y git

WORKDIR CAM_SUPERVISION
# Requirement
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#création des répertoires
RUN mkdir ./log && mkdir ./static && mkdir ./conf

# configuration
EXPOSE 5002
ENV FLASK_APP=main.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]