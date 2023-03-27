#!/bin/sh
#
# You'll need a valid cookie, sessionid, and csrf tokens
# These can be found using DevTools, burp, or ZAP
_csrf=''
_sessionid=''
_csrf2=''
_url='https://hack.ainfosec.com/challenge/submit-answer/'

# Discover Valid characters
_found=()
for _char in {a..z} {A..Z} {0..9}; do
	_str=`printf "${_char}%.0s" {1..7}`

	_score=`curl -sk -X POST ${_url} \
		-H "cookie: csrftoken=${_csrf}; sessionid=${_sessionid}" \
		-d "csrfmiddlewaretoken=${_csrf2}&challenge_id=code_breaker&answer=${_str}" | jq '.hc_challenge.score'`

	if [ ${_score} != 0 ]; then
		echo "${_str} = ${_score}"
		# Store found character
		_found+=("${_char}")
	fi
done
echo "Valid Chars: ${_found[@]}"

# Find valid character positions
_solution=("0" "0" "0" "0" "0" "0" "0") # placeholder
_mask='0000000' # we know that 0 is not a valid character
for _char in "${_found[@]}"; do
	for _pos in {1..7}; do
		_str=`echo ${_mask} | sed "s/./${_char}/${_pos}"`

		_score=`curl -sk -X POST ${_url} \
			-H "cookie: csrftoken=${_csrf}; sessionid=${_sessionid}" \
			-d "csrfmiddlewaretoken=${_csrf2}&challenge_id=code_breaker&answer=${_str}" | jq '.hc_challenge.score'`

		if [ ${_score} != 0 ]; then
			_idx=$((${_pos} - 1)) # index
			_solution[$_idx]=${_char}
			echo "${_char} : ${_str} = ${_score}"
		fi

	done
done
echo "Solution: ${_solution[@]}"
