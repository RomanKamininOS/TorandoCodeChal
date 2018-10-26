FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Install our requirements.
ADD . /srv/
WORKDIR /srv/
RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["bash", "entrypoint.sh"]
EXPOSE 8080