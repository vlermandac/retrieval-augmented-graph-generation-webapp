FROM debian:stable

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN mkdir -p build

WORKDIR /app/build

RUN cmake ..

RUN cmake --build .

ENTRYPOINT ["./KnowledgeGraph"]
