FROM continuumio/miniconda3:latest

WORKDIR /app

COPY . /app

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "llmenv", "/bin/bash", "-c"]

EXPOSE 8000
