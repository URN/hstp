#! /bin/sh

if [ -e /changed ]; then
    timeSinceMod=$(($(date +%s) - $(date +%s -r /changed)))
    if [ $timeSinceMod -gt 600 ]; then
        if [ ! -e /active]; then
            touch /active
            python -m hstp -i /input -o /output
            rm /changed /active
        fi
    fi
fi
