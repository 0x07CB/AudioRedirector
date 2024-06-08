FROM arm64v8/ubuntu:22.04
LABEL maintainer="0x07cb"
#ENV DEBIAN_FRONTEND noninteractive

# Install package dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        alsa-base \
        alsa-utils \
        libsndfile1-dev

#RUN apt-get install -y \
#        gettext \
#        unzip \
#        curl \
#        wget \
#        cmake \
#        make \
#        gcc \
#        ninja-build \
#        build-essential \
#        shfmt

#    apt-get clean

RUN apt-get install -y \
    python3 \
    python3-venv \
    python3-pip 

RUN apt-get install -y \
    portaudio19-dev 

# create a new user (without root privileges)
# username: appuser
# password: appuser
# With a home directory
# With a group with the same name
# With a shell: /bin/sh 
RUN useradd -U -m -s /bin/sh appuser
# add appuser to the audio group
RUN usermod -a -G audio appuser
# change password for appuser
RUN echo "appuser:appuser" | chpasswd
USER appuser
WORKDIR /home/appuser
RUN python3 -m venv env
USER root
WORKDIR /home/appuser
RUN chown -R appuser:appuser env
RUN chmod a+x env/bin/activate
USER appuser

# Add '/home/appuser/.local/bin' to the PATH
ENV PATH="/home/appuser/env/bin:$PATH"


RUN ./env/bin/activate \ 
    && python3 -m pip install --upgrade pip \ 
    && python3 -m pip install --no-cache-dir --upgrade numpy soundfile sounddevice 
    #&& python3 -m pip install --no-warn-script-location --no-cache-dir --upgrade numpy soundfile sounddevice

# copy the source code
COPY --chown=appuser:appuser ./app /home/appuser/app





USER root
WORKDIR /root
# Nettoie le cache APT et supprime les paquets inutiles
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*



USER appuser
WORKDIR /home/appuser
# the app need to load the virtual environment at '/home/appuser/env/bin/activate'
# the app is the script 'app.py' in the folder '/home/appuser/app'
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/appuser/env/bin/activate && python3 /home/appuser/app/app.py", "$@"]
