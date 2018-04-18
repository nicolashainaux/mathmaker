FROM ubuntu:17.10

LABEL maintainer="nh.techn@gmail.com"

# Install third-party dependencies
RUN apt-get -qq update
RUN apt-get install -y python3.6 python3-pip eukleides libxml2-utils gettext \
    texlive-latex-base texlive-luatex texlive-latex-recommended texlive-xetex \
    texlive-pstricks texlive-font-utils texlive-latex-extra texlive-base \
    texlive-science texlive-pictures texlive-generic-recommended \
    texlive-fonts-recommended texlive-fonts-extra locales
RUN apt-get clean

## Create directories for required files
RUN mkdir -p /build/ && mkdir -p /root/.mathmaker/outfiles/

## Generate locales (required for the tests)
RUN locale-gen en_US.UTF-8 && locale-gen fr_FR.UTF-8

## Add files required for the build
COPY requirements.txt setup.py CONTRIBUTORS.rst CHANGELOG.rst LICENSE MANIFEST.in  README  README.rst  mathmaker  pytest.ini /build/
COPY mathmaker /build/mathmaker/
COPY tests /build/tests/

## Run pip
RUN pip3 install --force -r /build/requirements.txt \
    --extra-index-url https://mirror.picosecond.org/pypi/simple && \
    pip3 install pytest coverage coveralls
