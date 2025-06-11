FROM python:3.9
WORKDIR /ContentSense
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements
COPY ..
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000","--reload"]