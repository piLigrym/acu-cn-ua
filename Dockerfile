FROM library/python:3.7.0
RUN pip install --upgrade pip
RUN mkdir -p /app
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000