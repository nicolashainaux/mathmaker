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

## Generate locales (required for the tests)
RUN locale-gen en_US.UTF-8 && locale-gen fr_FR.UTF-8

## Create directories for required files
RUN mkdir -p /root/.mathmaker/outfiles/
## Files required for the build should be copied as /mathmaker/ at build time

## Run pip
RUN pip3 install pytest coverage
# As mathmaker/requirements.txt is not available yet, it is still required
# to pip3 install these requirements before build time.
