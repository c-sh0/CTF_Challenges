#!/bin/sh
#
_key=${1}
for i in {0001..9999}; do
	_hash=`echo -n $i | openssl dgst -sha256 | awk '{print $2}'`
	if [ ${_hash} == ${_key} ]; then
		echo 'Found!'
		echo "PIN: $i ($_hash)" && exit 1
	fi
	echo -n '.'
done

