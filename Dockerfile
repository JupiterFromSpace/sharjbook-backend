FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip3 install \
    --default-timeout=300 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt


COPY ./core /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]