FROM python:3

WORKDIR /semantive

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG DB
ENV DATABASE_URL=$DB
ARG test
ENV BUILD_ENV=$test

RUN echo $(python -m unittest test/ml/TextServiceTest.py)
RUN echo $(python -m unittest test/ml/ImageServiceTest.py)

CMD [ "python", "./run.py" ]