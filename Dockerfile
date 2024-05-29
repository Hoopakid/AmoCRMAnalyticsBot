FROM python:3.10-alpine
WORKDIR /app

# Install Rust
RUN apk add --no-cache curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    source $HOME/.cargo/env && \
    apk add --no-cache musl-dev gcc

COPY . .

RUN pip install --upgrade pip
RUN source $HOME/.cargo/env && pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py"]
