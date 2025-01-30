#!/bin/bash

grep -vE "^#.*$" $1 | awk '/^$/ {print "*"} NF {print $3"\t"$4"\t"$5}' > $2