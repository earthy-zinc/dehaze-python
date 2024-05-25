FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
      wget \
      build-essential \
      libreadline-gplv2-dev \
      libncursesw5-dev \
      libssl-dev \
      libsqlite3-dev \
      tk-dev \
      libgdbm-dev \
      libc6-dev \
      libbz2-dev \
      libffi-dev \
      zlib1g-dev \
      && rm -rf /var/lib/apt/lists/* \
    && wget https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz \
    && tar xzf Python-3.11.8.tgz \
    && cd Python-3.11.8 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && rm -rf ../Python-3.11.8.tgz \
    && update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 \
    && update-alternatives --set python /usr/local/bin/python3.11
# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code && mkdir /pip_cache

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
ENV PIP_CACHE_DIR=/pip_cache

WORKDIR /code
VOLUME /code/trained_model

# 将所有文件复制到容器的 code 目录
ADD . /code/

# 更新 pip 并设置清华源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements_cpu.txt

CMD gunicorn dehazing_system.wsgi:application --bind 0.0.0.0:80 --workers 2

EXPOSE 80
