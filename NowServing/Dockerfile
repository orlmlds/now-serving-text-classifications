FROM python:3.6.3



WORKDIR /usr/app


# Let's copy and install requirements first so we don't need to do this every time the image builds
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy over the rest of the files we need to run and set up the application
COPY ./flaskr ./flaskr
COPY lib ./lib

COPY ./.env ./.env
COPY ./models ./models

EXPOSE 3000

ENTRYPOINT ["python", "flaskr/app.py"]


# To build docker image From /NowServing
# docker build -t now_serving
#