#!/bin/sh
#
# Credit:
# https://unix.stackexchange.com/questions/98948/ascii-to-binary-and-binary-to-ascii-conversion-tools
#
chrbin() {
        echo $(printf \\$(echo "ibase=2; obase=8; $1" | bc))
}

ordbin() {
	a=$(printf '%d' "'$1")
	echo "obase=2; $a" | bc
}

ascii2bin() {
	echo -n $* | while IFS= read -r -n1 char; do
		ordbin $char | tr -d '\n'
		echo -n " "
	done
	echo ''
}

bin2ascii() {
	for bin in $*; do
		chrbin $bin | tr -d '\n'
	done
	echo ''
}

bin2ascii ${1}

