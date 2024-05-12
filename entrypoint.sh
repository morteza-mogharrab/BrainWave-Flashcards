#!/bin/bash

if [ ! -f /src/db/cards.db ]; then
	cp cards-empty.db /src/db/cards.db
fi

export CARDS_SETTINGS=/src/config.txt
gunicorn --bind  0.0.0.0:5040 flash_cards:app