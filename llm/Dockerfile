FROM ollama/ollama:latest

WORKDIR /app
ARG LLM_MODEL
ARG LLM_PORT
ENV LLM_MODEL=${LLM_MODEL}
ENV LLM_PORT=${LLM_PORT}
ENV OLLAMA_HOST="0.0.0.0:${LLM_PORT}"

RUN apt-get update && apt-get install -y curl

COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh && /app/setup.sh