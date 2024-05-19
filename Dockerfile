FROM python:3.11-slim

WORKDIR /dashboard

# Copy the requirements file.
COPY requirements.txt ./requirements.txt

# Install virtualenv
RUN pip install virtualenv

# Create and activate a virtual environment.
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies into the virtual environment.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./dashboard/app.py /dashboard/

EXPOSE 8501

CMD [ "streamlit", "run", "app.py"]