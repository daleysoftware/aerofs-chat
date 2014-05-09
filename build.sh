#!/bin/bash
#
# This scripts builds a distributable `aerochat` executable that is comptabile with Mac OS X and
# common Linux distributions.

set -eu
cd $(dirname $0)/src

rm -f aerochat.zip $(find . | grep pyc)
zip -rq aerochat.zip __main__.py aerochat/*

encoded=$(cat aerochat.zip | openssl base64 -e)

cat > aerochat.sh <<EOF
#!/bin/bash
set -eu
cd \$(dirname \$0)
mkdir -p .aerochat/messages
cd .aerochat
echo "$encoded" | openssl base64 -d > aerochat.zip
python aerochat.zip &
disown
exit 0
EOF

chmod a+x aerochat.sh
mv aerochat.sh ../aerochat
rm aerochat.zip
