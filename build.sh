#!/bin/bash
#
# This scripts builds a distributable `aerochat` executable that is comptabile with Mac OS X and
# common Linux distributions.

set -eu
cd $(dirname $0)/src

rm -f aerochat.zip
zip -q aerochat.zip __main__.py aerochat/*

encoded=$(cat aerochat.zip | openssl base64 -e)

cat > aerochat.sh <<EOF
#!/bin/bash
set -eu
clear
cd \$(dirname \$0)
mkdir -p .aerochat
cd .aerochat
if [ ! -f aerochat.zip ]
then
    echo "$encoded" | openssl base64 -d > aerochat.zip
fi
python aerochat.zip
EOF

chmod a+x aerochat.sh
mv aerochat.sh ../aerochat
rm aerochat.zip
