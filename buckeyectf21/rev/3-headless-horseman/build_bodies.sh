#!/bin/bash

if [ ! -d frankensteins ]; then
    mkdir frankensteins
fi
for head in ./*_head; do
    for body in ./body_bag/*_body; do
        cat $head $body > frankensteins/`basename $head`_`basename $body`
    done
done
chmod +x ./frankensteins/*

