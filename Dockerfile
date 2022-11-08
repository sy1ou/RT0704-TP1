FROM python:3.11

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

WORKDIR /srv

COPY ./requirements.txt /srv/requirements.txt
COPY ./gunicorn_conf.py /srv/gunicorn_conf.py

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
EXPOSE 8000

ENTRYPOINT ["gunicorn", "--config", "gunicorn_conf.py"]
CMD ["app.main:app"]
