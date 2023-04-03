FROM python:3.11-slim

RUN mkdir -p /realtime-events

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH="${PYTHONPATH}:/realtime-events"

# Needed for Fast API 
ENV WATCHFILES_FORCE_POLLING=true

# Only for Local Environment
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

COPY . /realtime-events

RUN pip install --no-cache-dir --upgrade -r /realtime-events/requirements.txt
RUN pip install debugpy

WORKDIR /realtime-events