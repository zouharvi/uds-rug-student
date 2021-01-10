#!/bin/bash

python3 ./src/aligner.py -n 100000 -e A0+NULL -s 5 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -e A0 -s 5 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -e A2 -s 7 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -e A3 -s 7 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -e A4 -s 7 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -e A2*A3*A4 -s 7 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -d -e A2*A3*A4*diag -s 5 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10
# python3 ./src/aligner.py -n 100000 -d -e A2*A3*A4*diag -s 10 | python3 ./jhu-mt-hw/hw2/score-alignments --data jhu-mt-hw/hw2/data/hansards -n 10