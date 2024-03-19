FROM python:3.9.18-alpine3.19

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# /tmp 目录就会在运行时自动挂载为匿名卷，任何向 /tmp 中写入的信息都不会记录进容器存储层
VOLUME /tmp

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code
# 将所有文件复制到容器的 code 目录
ADD . /code/

# 更新 pip 并设置清华源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements_cpu.txt

CMD gunicorn dehazing_system.wsgi:application --bind 0.0.0.0:8080 --workers 2

EXPOSE 8080
# 时区修改
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' >/etc/timezone; \
    echo -e https://mirrors.ustc.edu.cn/alpine/v3.7/main/ > /etc/apk/repositories; \
    apk --no-cache add ttf-dejavu fontconfig
