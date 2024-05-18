FROM python:3.11

WORKDIR /dashboard

COPY requirements.txt /dashboard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /dashboard/requirements.txt 

COPY ./app.py /dashboard/

EXPOSE 8501

CMD [ "streamlit", "run", "app.py"]