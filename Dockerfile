FROM python:3.13.0a6-alpine3.18
LABEL authors="ZKWolf"

RUN apk upgrade && apk add curl
RUN mkdir -p /app/
RUN mkdir -p /app/src
RUN mkdir -p /app/src/logic
RUN mkdir -p /app/src/endpoints

WORKDIR /app/src

COPY requirements.txt /app/src/requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY src/start_app.py /app/src/start_app.py
COPY src/flask_definitions.py /app/src/flask_definitions.py

COPY src/config/ /app/src/config/

COPY src/endpoints/aes.py /app/src/endpoints/aes.py
COPY src/endpoints/general.py /app/src/endpoints/general.py
COPY src/endpoints/unknown.py /app/src/endpoints/unknown.py
COPY src/endpoints/user_handeling.py /app/src/endpoints/user_handeling.py
# Future idea? ^
COPY src/endpoints/web.py /app/src/endpoints/web.py

COPY src/static/ /app/src/static/
COPY src/templates/ /app/src/templates/

COPY src/logic/date_handler.py /app/src/logic/date_handler.py
COPY src/logic/global_handler.py /app/src/logic/global_handler.py
COPY src/logic/logging_handler.py /app/src/logic/logging_handler.py
COPY src/logic/mongodb_handler.py /app/src/logic/mongodb_handler.py
COPY src/logic/setup_handlers.py /app/src/logic/setup_handlers.py
COPY src/logic/webhook_handler.py /app/src/logic/webhook_handler.py

COPY src/bms/ /app/src/bms/

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/api/v1/healthcheck

ENTRYPOINT ["python", "start_app.py"]