FROM python:3.10.8
WORKDIR /code
COPY ./requirements ./requirements
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/common.txt
COPY . /code
ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]