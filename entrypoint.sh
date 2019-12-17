#!/bin/sh

if [ "$(id -u)" = '0' ]; then
    find "$LOG_DIR" \! -user www -exec chown www '{}' +
fi

exec "$@"