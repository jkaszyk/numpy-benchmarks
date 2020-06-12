#!/bin/bash

sed -i '.bak' 's/\(#setup: \)\(.*\)/def data(np):\n    \2/' $1
sed -i '.bak' 's/\;/\n   /g' $1

