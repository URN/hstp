#! /bin/sh

crond

inotifywait -m /input -e create -e moved_to |
    while read directory action file; do
        touch /changed
    done