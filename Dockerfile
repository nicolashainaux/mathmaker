FROM ubuntu:17.10

MAINTAINER nicolashainaux "https://github.com/nicolashainaux"

# Install third-party dependencies
RUN apt-get -qq update
RUN apt-get install -y python3.6 python3-pip eukleides libxml2-utils gettext \
    texlive-latex-base texlive-luatex texlive-latex-recommended texlive-xetex \
    texlive-pstricks texlive-font-utils texlive-latex-extra texlive-base \
    texlive-science texlive-pictures texlive-generic-recommended \
    texlive-fonts-recommended texlive-fonts-extra
RUN rm -rf /var/lib/apt/lists/*

## Create a directory for required files
RUN mkdir -p /build/

## Add files required for the build
COPY requirements.txt setup.py mathmaker/ tests/ /build/

## Run pip
RUN cd /build/
RUN pip3 install --force -r requirements.txt --extra-index-url https://mirror.picosecond.org/pypi/simple
RUN pip3 install coverage coveralls
