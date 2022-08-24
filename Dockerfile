# #./Dockerfile

# #기반이 될 이미지
# FROM python:3.9

# # 작업디렉토리(default)설정
# WORKDIR /Users/han/desktop/projects/borikkori

# ## Install packages

# # 현재 패키지 설치 정보를 도커 이미지에 복사
# COPY requirements.txt ./ 

# # 설치정보를 읽어 들여서 패키지를 설치
# RUN pip install -r requirements.txt

# # Konlpy 사용을 위한 JDK 설치
# RUN apt-get install -y default-jdk default-jre

# ## Copy all src files

# # 현재경로에 존재하는 모든 소스파일을 이미지에 복사
# COPY . . 

# ## Run the application on the port 8080

# # 8000번 포트를 외부에 개방하도록 설정
# EXPOSE 8000   

# # CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"]
# # gunicorn을 사용해서 서버를 실행
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "branchtime.wsgi:application"]


FROM ubuntu:latest

ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

RUN apt-get install -y default-jdk default-jre

RUN apt-get install -y python3-pip python3-dev

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip3 install --upgrade pip

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /workspace
WORKDIR /workspace

RUN pip install jpype1-py3 konlpy

ENV WSGIPath config/wsgi.py

COPY ./requirements.txt /code/requirements.txt

RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /code/
WORKDIR /code/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "borikkori.wsgi:application"]