FROM python:3.11


WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY . /app


# Install dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy the entire application code


# Copy the enviroments variables
#COPY .env .env

# Expose the port your application will run on
EXPOSE 8080

#Initializaing Waitress Server
#CMD python -m flask --app app/__init__.py run --host 0.0.0.0 --port 8080 --debug
CMD waitress-serve --host 0.0.0.0 --call app:create_app 

