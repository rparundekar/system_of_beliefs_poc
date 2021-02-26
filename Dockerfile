FROM python:3.8-slim-buster

RUN apt-get -y update && apt-get install -y --no-install-recommends build-essential \
        wget \
        nginx \
        ca-certificates \
        software-properties-common \
        zip \
        && apt-get clean && rm -rf /tmp/* /var/tmp/*
    
RUN pip install --upgrade pip

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/app:${PATH}"

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set up the program in the image
COPY app /app
WORKDIR /app

# Expose port
EXPOSE 8080

# Add non-root user
RUN groupadd -r user && useradd -r -g user user
RUN chown user /app /var/log/nginx /var/lib/nginx /tmp
USER user

