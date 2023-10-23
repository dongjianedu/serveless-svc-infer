# Use specific version of nvidia cuda image
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

# Set shell and noninteractive environment variables
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

# Set working directory
WORKDIR /

# Update and upgrade the system packages (Worker Template)
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install --yes --no-install-recommends sudo ca-certificates git wget curl bash libgl1 libx11-6 software-properties-common ffmpeg build-essential libssl-dev libasound2  cmake -y &&\
    curl 'http://pan.mytunnel.top/?explorer/share/file&hash=b9bdvDBNIjyesDJzu5VZBLDEnrEkv0kcW9pChJ7uc_IKPugmnrj9cke_24zhe4tdZw' -o 'checkpoint_best_legacy_500.pt' && \
    curl 'http://pan.mytunnel.top/?explorer/share/file&hash=e22bp7HDbZf8OMpivavRIBX5Cc996MVbgas_ZeXPh4KktWxr8nTMDY6rRJnKWOgh5Q' -o 'G_125600.pth' && \
    curl 'http://pan.mytunnel.top/?explorer/share/file&hash=5e55WH7qyLtw-EGxsHPyeShGKN0_ZnUFe5LXWSg9IATpdAahB3SxKKYUqln2Ox4jZg' -o 'model' && \
    curl 'http://pan.mytunnel.top/?explorer/share/file&hash=44a98cr7LOBkMhvpwzPgG_NLZLiD3jVZ_-stEAXY0NC_bGnvnZ2_2liIXMypSDgtrQ' -o 'rmvpe.pt' && \
    wget -O 'cmake-3.22.1.tar.gz' 'http://pan.mytunnel.top/?explorer/share/file&hash=4ef30G-sb1cAZr6a5GtmhrudUg7vPhf0IzOpJ3fC0hX7ox0HJUi4kUKTlrj6Q-UmRw' && \
    tar -xvzf cmake-3.22.1.tar.gz -C /usr/share/ && \
    cd /usr/share/cmake-3.22.1 && \
    ./configure && \
    chmod 777 ./configure && \
    make  -j4&& \
    make install && \
    update-alternatives --install /usr/bin/cmake cmake /usr/local/bin/cmake 1 --force && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Add the deadsnakes PPA and install Python 3.10
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python3.10-dev python3.10-venv python3-pip -y --no-install-recommends  && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.10 /usr/bin/python3 && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Download and install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r /requirements.txt --no-cache-dir   && \
    rm /requirements.txt





# Copy source code into image
COPY src .

RUN mv /checkpoint_best_legacy_500.pt /pretrain/checkpoint_best_legacy_500.pt && \
    mv /G_125600.pth /logs/44k/G_125600.pth && \
    mv /model /pretrain/nsf_hifigan/model && \
    mv /rmvpe.pt /pretrain/rmvpe.pt && \
    rm /checkpoint_best_legacy_500.pt && \
    rm /G_125600.pth && \
    rm /nsf_hifigan/model && \
    rm /mvpe.pt



# Set default command
CMD python -u /rp_handler.py
