#!/usr/bin/env bash
if [[ ! -z "$(docker ps --filter 'name=BrainWave-Flashcards' -q)" ]]; then
    docker stop BrainWave-Flashcards
fi
