#!/usr/bin/env bash

# # https://postgrest.org/en/stable/tutorials/tut1.html
# https://www.willhaley.com/blog/generate-jwt-with-bash/

#
# JWT Encoder Bash Script
#

# Allow "tr" to process non-utf8 byte sequences
export LC_CTYPE=C

# read random bytes and keep only alphanumerics
secret="$(< /dev/urandom tr -dc A-Za-z0-9 | head -c32)"
echo "SERVER_JWT_SECRET=\"${secret}\"" >> jwt.conf

# Static header fields.
header='{
	"typ": "JWT",
	"alg": "HS256",
	"kid": "0001",
	"iss": "Bash JWT Generator"
}'

# Use jq to set the dynamic `iat` and `exp`
# fields on the header using the current time.
# `iat` is set to now, and `exp` is now + 1 second.
# header=$(
# 	echo "${header}" | jq --arg time_str "$(date +%s)" \
# 	'
# 	($time_str | tonumber) as $time_num
# 	| .iat=$time_num
# 	| .exp=($time_num + 1)
# 	'
# )
payload='{
	"role": "api_user"
}'

base64_encode()
{
	declare input=${1:-$(</dev/stdin)}
	# Use `tr` to URL encode the output from base64.
	printf '%s' "${input}" | base64 | tr -d '=' | tr '/+' '_-' | tr -d '\n'
}

json() {
	declare input=${1:-$(</dev/stdin)}
	printf '%s' "${input}" | jq -c .
}

hmacsha256_sign()
{
	declare input=${1:-$(</dev/stdin)}
	printf '%s' "${input}" | openssl dgst -binary -sha256 -hmac "${secret}"
}

header_base64=$(echo "${header}" | json | base64_encode)
payload_base64=$(echo "${payload}" | json | base64_encode)

header_payload=$(echo "${header_base64}.${payload_base64}")
signature=$(echo "${header_payload}" | hmacsha256_sign | base64_encode)

echo "SERVER_JWT_TOKEN=\"${header_payload}.${signature}\"" >> jwt.conf