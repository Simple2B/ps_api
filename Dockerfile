FROM python:3.12

ARG APP_PORT=8080

# Add user app
RUN python -m pip install -U pip
RUN adduser -uid 1000 app
USER app
WORKDIR /home/app

# set environment varibles
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV APP_PORT=${APP_PORT}

# install poetry
# RUN pip install poetry
RUN pip install --user poetry
ENV PATH="/home/app/.local/bin:${PATH}"


# install app dependencies
COPY --chown=app:app poetry.lock .
COPY --chown=app:app pyproject.toml .
COPY --chown=app:app poetry.toml .


RUN poetry install --only main -n --no-ansi
RUN poetry add uvicorn

COPY --chown=app:app . .

RUN chmod +x ./start_web.sh
CMD ["./start_web.sh"]

EXPOSE ${APP_PORT}
