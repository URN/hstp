#! /bin/sh

if [ -e /changed ]; then
    timeSinceMod=$(($(date +%s) - $(date +%s -r /changed)))
    if [ $timeSinceMod -gt 600 ]; then
        python -m hstp -i /input -o /output
        rm /changed
    fi
fi
