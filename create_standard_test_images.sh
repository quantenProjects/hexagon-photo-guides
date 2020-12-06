#!/bin/bash

for i in "2700x1905" "3600x2540" "4500x3175" "5400x3810" "6300x4445"
do
	echo $i
	python measurment_picture.py -g $i -m 0,150,5 --test-lines-bw -b lightgrey --print-args -c v1 /tmp/test-$i.png
done
