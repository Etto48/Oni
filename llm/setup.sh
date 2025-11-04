#!/bin/bash

set -e
ollama serve &
PID=$!

while ! ollama list &>/dev/null; do
    echo "Waiting for Ollama to start..."
    sleep 1
done

ollama pull $LLM_MODEL

kill $PID