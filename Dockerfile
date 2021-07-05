FROM python:3.7

RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80

RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml

WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["app/app.py"]
