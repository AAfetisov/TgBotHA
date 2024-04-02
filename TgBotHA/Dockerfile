ARG BUILD_FROM
FROM python:3.8

WORKDIR /bot
RUN pip install --no-cache-dir pyTelegramBotAPI

# Copy data for add-on
COPY . .
RUN chmod a+x /bot/run.sh

CMD ["/bot/run.sh"]