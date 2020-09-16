#################################################
# Data Science Base Dockerfile 
# 
# Base Docker image: tensorflow/tensorflow:latest-gpu-py3
# User: root (for simplicity)
#################################################

# Base docker image
FROM tensorflow/tensorflow:latest-gpu-py3


# Timezone and Maintainer info
ENV TZ Asia/Tokyo
MAINTAINER Qiulongquan

# Installing developer tools and video/image display optimizations
RUN apt-get update -yq && apt-get install sqlite3 -yq
RUN apt-get install lsof -yq
RUN apt-get install wget -yq
# RUN apt-get update -yq && apt-get install software-properties-common -yq
# RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
# RUN apt-get update -yq && \
# 	apt-get install -yq build-essential cmake git pkg-config wget unzip vim && \
# 	apt-get install -yq libjpeg-dev libtiff5-dev libjasper1 libjasper-dev libpng12-dev libpng16-16 && \
# 	apt-get install -yq libavcodec-dev libavformat-dev libswscale-dev libv4l-dev && \
# 	apt-get install -yq libxvidcore-dev libx264-dev && \
# 	apt-get install -yq libgtk-3-dev && \
# 	apt-get install -yq libhdf5-serial-dev graphviz && \
# 	apt-get install -yq libopenblas-dev libatlas-base-dev gfortran && \
# 	apt-get install -yq libcanberra-gtk-module && \
# 	apt-get install -yq python-tk python3-tk python-imaging-tk && \
# 	apt-get install -yq python3 python3-dev && \
# 	apt-get install -yq python3-pip python3-setuptools && \
# 	wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

# Miniconda install and env set
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
#     /bin/bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
#     rm Miniconda3-latest-Linux-x86_64.sh && \
#     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
# ENV PATH $PATH:/opt/conda/bin

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc


# Expose ports 22: ssh,  jupyter nb: 8080, django: 8000
EXPOSE 22
EXPOSE 80
EXPOSE 8000
EXPOSE 8080

# Changing work directory to workspace
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip install -r requirements.txt

COPY . /workspace/
# using CMD command to run, page contents will automatic show on the web page
CMD python3 /workspace/manage.py runserver 0.0.0.0:8000

# Commands 
# CMD [ "/bin/bash" ]
