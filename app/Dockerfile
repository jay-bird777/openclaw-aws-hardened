FROM python:3.12-slim
WORKDIR /app
COPY main.py /app/main.py
RUN pip install --no-cache-dir discord.py
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
CMD ["python", "/app/main.py"]
