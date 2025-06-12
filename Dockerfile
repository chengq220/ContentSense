FROM python:3.9
WORKDIR /ContentSense
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ARG HF_TOKEN
ENV HF_TOKEN=$HF_TOKEN
COPY model_download.py ./
RUN python model_download.py
COPY . .
CMD ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000","--reload"]