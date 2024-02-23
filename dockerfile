FROM python:3
COPY requirements.txt ./
EXPOSE 8081
RUN pip install --no-cache-dir -r requirements.txt
COPY .. .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8081", "app:app"]
