#! /bin/sh

crond

inotifywait -m /input -r |
    while read directory action file; do
        touch /changed
    done
