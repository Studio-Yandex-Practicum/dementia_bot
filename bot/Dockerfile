FROM ghcr.io/withlogicco/poetry:1.6.1

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY ./ ./

CMD ["python", "main.py"]
