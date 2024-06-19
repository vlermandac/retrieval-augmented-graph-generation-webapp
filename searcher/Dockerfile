FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY . /app
RUN conda install --channel=conda-forge --name=base conda-lock
RUN conda-lock install -n env conda-lock.yml

# Make RUN commands use the new environment:
RUN echo "conda activate env" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN chmod +x /app/entrypoint.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
