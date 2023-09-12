FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt update -y && apt install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN $HOME/.local/bin/poetry config virtualenvs.create false
RUN $HOME/.local/bin/poetry install

COPY ./ ./

CMD ["gunicorn", "expert_system.wsgi:application", "--bind", "0:8000" ] 
