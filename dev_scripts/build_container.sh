#!/usr/bin/env bash
if [[ ! -z "$(docker images BrainWave-Flashcards -q)" ]]; then
	docker rmi BrainWave-Flashcards
fi
docker build -t BrainWave-Flashcards .