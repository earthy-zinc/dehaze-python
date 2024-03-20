FROM python:3.11

# /tmp 目录就会在运行时自动挂载为匿名卷，任何向 /tmp 中写入的信息都不会记录进容器存储层
VOLUME /tmp

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code && mkdir /pip_cache

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
ENV PIP_CACHE_DIR=/pip_cache

WORKDIR /code

# 将所有文件复制到容器的 code 目录
ADD . /code/

# 更新 pip 并设置清华源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements_cpu.txt

CMD gunicorn dehazing_system.wsgi:application --bind 0.0.0.0:80 --workers 2

EXPOSE 80
