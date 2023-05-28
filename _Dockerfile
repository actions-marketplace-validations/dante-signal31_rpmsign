#ARG dev_build
ENV dev_build=0

#FROM fedora:38 AS base
## Image metadata.
#LABEL maintainer="dante-signal31 (dante.signal31@gmail.com)"
#LABEL description="Image to run rpmsign GitHub Action."
#LABEL homepage="https://github.com/dante-signal31/rpmsign"
#
#ENV virtualenv=/root/venv
#
#RUN echo "Configuring basic environment..."
#
## Abort on error.
#RUN set -e
#
## Copy configuration for gpg-agent.
#COPY gpg-agent.conf /root/.gnupg/
#
#
## Get system dependencies for this project.
#RUN yum update -y && \
#    yum install rpm-sign pinentry-tty python3-pip -y
#
## Create virtualenv.
##RUN python3 -m venv $virtualenv
#
#
## DEVELOPMENT VERSION
#FROM base AS version-1
#RUN echo "Configuring a development environment..."
#
## Get system dependencies to be run as a remote interpreter in Pycharm.
#RUN yum update -y && \
#    yum install which -y
#
## Set folder for our development configuration.
#ENV DEV_PATH /root/dev
#
## Get script development dependencies.
#COPY dev-requirements.txt $DEV_PATH/
#RUN pip install --no-cache-dir -r $DEV_PATH/dev-requirements.txt
#
## Get script dependencies.
#COPY requirements.txt $DEV_PATH/
#RUN pip install --no-cache-dir -r $DEV_PATH/requirements.txt
#
#
## RELEASE VERSION
#FROM base AS version-0
#RUN echo "Configuring a release environment..."
#
## Set folder for our script.
#ENV SCRIPT_PATH /root/script
#
## Get script dependencies.
#COPY requirements.txt $SCRIPT_PATH/
#RUN pip install --no-cache-dir -r $SCRIPT_PATH/requirements.txt
#
## Copy scripts to image folder.
#COPY src/lib/* $SCRIPT_PATH/lib/
#COPY src/rpmsign.py $SCRIPT_PATH/
## Make it globally executable.
#RUN chmod 755 $SCRIPT_PATH/rpmsign.py && \
#    ln -s $SCRIPT_PATH/rpmsign.py /usr/bin/rpm_sign
#
## Set rpm_sign as this image entrypoint
#ENTRYPOINT ["rpm_sign"]
#
#
## FINAL BUILD VERSION
#FROM version-${dev_build} AS final
#RUN echo "Environment ot type ${dev_build} ready"