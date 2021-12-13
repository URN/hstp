#! /bin/bash

if [ -e /changed ]; then
    timeSinceMod=$(($(date +%s) - $(date +%s -r /changed)))
    if [ $timeSinceMod -gt 600 ]; then
        if [ ! -e /active ]; then
            touch /active
            date >> /log
            python -m hstp -i /input -o /output &>> /log
            rm /changed /active
        fi
    fi
fi
