#!/bin/bash

python3 ./src/aligner.py -d -n 100000 -e A2*A3*A4*int -s 5 --file1 'jhu-mt-hw/hw2/data/hansards.e' --file2 'jhu-mt-hw/hw2/data/hansards.f' > /tmp/algn.fw
python3 ./src/aligner.py -d -n 100000 -e A2*A3*A4*int -s 5 --file1 'jhu-mt-hw/hw2/data/hansards.f' --file2 'jhu-mt-hw/hw2/data/hansards.e' > /tmp/algn.bw
python3 ./src/intersector.py /tmp/algn.{fw,bw} | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 1

rm /tmp/algn.{fw,bw}