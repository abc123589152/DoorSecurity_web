# 使用 Ubuntu 作為基礎映像
FROM ubuntu:latest

# 更新包列表並安裝必要的工具
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    git

# 安裝 Python 3.11.5
RUN wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz \
    && tar xzf Python-3.11.5.tgz \
    && cd Python-3.11.5 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.11.5 Python-3.11.5.tgz

# 確保使用的是 python3.11 版本
RUN ln -s /usr/local/bin/python3.11 /usr/bin/python3

# 更新 pip
RUN python3 -m pip install --upgrade pip

# 安裝 Python 庫
RUN pip install mysql-connector-python flask
