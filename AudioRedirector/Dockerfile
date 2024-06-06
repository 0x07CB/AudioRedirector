FROM arm64v8/python:3.10.14-alpine3.20
LABEL maintainer="0x07cb"


# update packages list
RUN apk update

# install required packages 
# ( 'gcc' and 'meason' )
# , please add 'libasound2' and 'libasound2-dev' to the list of packages
RUN apk add --no-cache \
    gcc \
    make \
    cmake \
    musl-dev \
    portaudio-dev \
    alsa-lib-dev \
    libffi-dev \
    libsndfile-dev \
    alsaconf \
    alsa-utils \
    alsa-lib \
    alsa-plugins-pulse \
    portaudio \
    libsndfile 


#musl-dev portaudio-dev alsa-lib-dev

# create a new user (without root privileges)
# username: appuser
# password: appuser
# I want this user have a home directory, and a group with the same name
RUN addgroup -S appuser && adduser -S appuser -G appuser -h /home/appuser -s /bin/sh
RUN addgroup $USER audio
RUN addgroup root audio
# change password for the user 'appuser'
RUN echo "appuser:appuser" | chpasswd
# change the password for the user 'root'
RUN echo "root:root" | chpasswd


USER appuser
WORKDIR /home/appuser
RUN python3 -m venv env \
    && source env/bin/activate \
    && python3 -m pip install --upgrade pip \ 
    && python3 -m pip install --no-warn-script-location --no-cache-dir --upgrade numpy soundfile sounddevice
 #&& pip install --no-cache-dir --upgrade numpy librosa matplotlib soundfile sounddevice tempfile

# copy the source code
COPY --chown=appuser:appuser ./app /home/appuser/app

# Add '/home/appuser/.local/bin' to the PATH
ENV PATH="/home/appuser/env/bin:$PATH"


ENTRYPOINT ["/bin/sh"]
#, "-c", "source env/bin/activate"]
#" && python3 app/redirect_audio_in_out.py"]


 
