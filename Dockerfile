# FROM python:3.11-slim
# WORKDIR /app
# COPY . /app
# RUN pip install --no-cache-dir -r requirements.txt || true
# CMD ["python", "main.py"]

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

EXPOSE 8080

ENV MODEL="hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"
ENV MODEL_OPTIONS="hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"
ENV LLM_URL="http://host.docker.internal:11434/v1/chat/completions"
ENV MAX_TOKENS="1024"
ENV KEEP_ALIVE="30m"
ENV PORT="8080"

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "120", "app:app"]

# EXPOSE 8080
# CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]


# ENV MODEL=glm-ocr