#!/bin/bash

paste jhu-mt-hw/hw2/data/hansards.f jhu-mt-hw/hw2/data/hansards.e | sed -e 's/\t/ ||| /g' > /tmp/parallel1

head -n 100000 /tmp/parallel1 > /tmp/parallel2

~/bin/fast_align/build/fast_align -d -o -v -i /tmp/parallel2 2> /dev/null | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10

rm /tmp/parallel{1,2}