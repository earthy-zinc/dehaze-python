## 项目介绍

项目基于 Python3.8、Django、Pytorch1.8.1 等技术栈搭建的前后端分离图像去雾系统，本代码为 python后端。

## 运行环境
* Ubuntu linux 系统
* 具有Cuda的显卡
* python 3.8
* pytorch 1.8.1

## 项目运行

```shell
# 克隆源码
git clone https://gitee.com/earthy-zinc/dehazing_python.git
# 进入程序根目录
cd dehazing_python
# 创建并激活python环境
conda env create -n dehaze_backend python=3.8
conda acticate dehaze_backend
# 安装依赖
conda install --yes --file requirements.txt
# 数据库迁移
python manage.py migrate
# 运行代码
BASICSR_JIT=True python manage.py rserver 0.0.0.0:9911
```
