#!/bin/bash

sed -i  -e 's/\(#setup: \)\(.*\)/def data(np):\n    \2/' $1
sed -i -e 's/\;/\n   /g' $1

