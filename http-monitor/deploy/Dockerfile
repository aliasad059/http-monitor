# pull official python image
FROM python:3.8-slim

# set working directory
ENV DockerHome=/home/services

# create the working directory
RUN mkdir -p ${DockerHome}

# copy the working directory
COPY requirements.txt ${DockerHome}

# set the working directory
WORKDIR ${DockerHome}

# upgrade pip
RUN pip install --upgrade pip

# install requirements
RUN pip install -r requirements.txt
    
# copy the working directory
COPY . ${DockerHome}

# add service environment variables
ENV PYTHONPATH ${DockerHome}
ENV PYTHONUNBUFFERED=1

# run the service
CMD cd ${DockerHome}/src && python main.py