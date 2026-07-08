# Local LLM Proxy

A professional, lightweight Flask-based API for routing chat requests to an LLM backend. This project demonstrates how to build a simple, containerized service that exposes health, configuration, and chat completion endpoints for local experimentation or integration into larger applications.

## Project Summary

This repository showcases a minimal backend architecture for working with large language models. It provides a clean interface for sending prompts to a configurable LLM endpoint while keeping the implementation easy to deploy, test, and extend.

## Key Features

- Flask-based REST API with `/health`, `/config`, and `/chat` endpoints
- Compatible with local and remote LLM backends
- Docker-ready deployment for consistent environments
- Configurable model selection, endpoint URL, token limits, and payload settings
- Simple structure suitable for learning, prototyping, and production-style integration

## Repository Structure

- `app.py` — Flask application and API routes
- `Dockerfile` — container build configuration
- `requirements.txt` — Python dependencies
- `body.json` and `chat_body.json` — example request payloads
- `chat.ps1` — PowerShell helper script for testing
- `README.md` — project documentation

## Local Development

```powershell
cd C:\Users\subham.adhikari\Documents\docker_ml
python -m pip install -r requirements.txt
python app.py
```

### Example Request

```powershell
curl.exe -v http://localhost:8080/chat -H "Content-Type: application/json" -d '{"prompt":"Hello","model":"gpt-5"}'
```

## Docker Deployment

```powershell
docker build -t llm-proxy .
docker run --rm --add-host=host.docker.internal:host-gateway -p 8080:8080 llm-proxy
```

### Custom Environment Configuration

```powershell
docker run --rm --add-host=host.docker.internal:host-gateway ^
  -e LLM_URL=http://host.docker.internal:11434/v1/chat/completions ^
  -e MODEL=gpt-5 ^
  -e MAX_TOKENS=1024 ^
  -p 8080:8080 llm-proxy
```

## Configuration

The application supports the following environment variables:

- `LLM_URL` — target LLM API URL
- `MODEL` — default model name
- `MODEL_OPTIONS` — comma-separated list of supported models
- `MAX_TOKENS` — maximum output tokens
- `KEEP_ALIVE` — keep-alive value sent with payloads
- `PORT` — port used by the Flask app

## Notes

- This project focuses on backend functionality and does not include a frontend interface.
- If your LLM server uses a different host or path, update `LLM_URL` accordingly.
- Sample payload files are included to simplify testing and validation.
