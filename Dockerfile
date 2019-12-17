FROM python:3.6.6

COPY ./src/requirements.txt /home/app/requirements.txt
RUN pip install --upgrade pip && pip install -r /home/app/requirements.txt

COPY ./entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

RUN addgroup www && adduser --system www && adduser www www
WORKDIR /home/www
COPY ./src /home/www

ENV LOG_DIR /log
RUN mkdir -p "$LOG_DIR" && chown -R www:www "$LOG_DIR"
VOLUME /log