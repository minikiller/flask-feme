FROM python:3.8
LABEL Maintainer="sunlingfeng & litao"

RUN mkdir -p /usr/src/app && mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir gunicorn && pip install --no-cache-dir -r /usr/src/app/requirements.txt

# 如果gunicorn启用grevent模式时需要安装这个包
RUN pip install -U --force-reinstall --no-binary :all: gevent

COPY . /usr/src/app
RUN chmod 755 *.sh 
# 需要暴漏给容器外的口 空格隔开可以多个端口
EXPOSE 8000
CMD ["bash","-c","./restart_gunicorn.sh"]
