# Writeup

We start off with three "bodies" (binary files) and an ELF `headless_horseman`. After running the ELF, the headless horseman will give us "heads" so we can reconstruct the heroes if we give him the right number of pumpkins. The correct number is `0xdeadface` (`3735943886`).

We now have an assortment of "heads". Looks like they are ELF headers. We will enumerate all possible body combinations with `build_bodies.sh`.

```bash
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
```

Running `file` on all the files tells us that these are the correct combinations:
- dessicated_head + decomposing_body = ichibod 
- moldy_head + bloated_body = katrina
- shrunken_head + rotting_body = brom

Each person will give us a part of the final flag. We use QEMU to emulate the MIPS/ARM binaries.

## Ichibod

Ichibod gives us his piece of the flag if the environment variable `ICHIBODS_HORSE` is present. We can also just base64 decode the encoded string found in the disassembly: `flag{the_horseman_just_`.

## Katrina

Katrina asks for the key she used to encrypt her secret. She states that it's likely her hometown. From the README.txt, we know this to be `Sleepy Hollow`. Her piece of the flag is `really_loves_`.

## Brom

Brom's puzzle is a simple stack overflow. His secret is printed if a stack variable matches a hardcoded value `"DEAD"`. We can retrieve the flag with 
```bash
echo "AAAAAAAAAAAAAAAAAAAADEAD" | ./brom
```
His secret is `pumpkin_pie}`.

# Solution

`flag{the_horseman_just_really_loves_pumpkin_pie}`

