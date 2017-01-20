#!/bin/bash

PARAM=2
PWD=`pwd`

E_ERR_ARG=65
E_NOFILE=66
E_NOTAG=67

DBFILE=$1
METADATAFILE=$2
UUID=`uuidgen -t`
if [ $# -ne "$PARAM" ]
    then
    echo
    echo "Usage: ./renameFiles.sh <sqlitefile> <metadatafile>"
    exit $E_ERR_ARG
fi

if [ ! -e "${DBFILE}" ]
    then
    echo
    echo "$DBFILE does not exist"
    exit $E_NOFILE
fi

if [ ! -e "$METADATAFILE" ]
    then
    echo
    echo "$METADATAFILE does not exist"
    exit $E_NOFILE
else
    TAGNAME=`cat $METADATAFILE | awk 'NR==4 { print $1 }' | tr -d '"' | tr -d ':'`
    if [ "$TAGNAME" = "" ]
	then
	echo "tag name non provided in the metadata file."
	exit $E_NOTAG
    fi
fi

#cp $DBFILE ${PWD}/${TAGNAME}@${UUID}.db
cp $DBFILE ${PWD}/${TAGNAME}.db
#cp $METADATAFILE ${PWD}/${TAGNAME}@${UUID}.txt
#chmod a+w ${PWD}/${TAGNAME}@${UUID}.txt
#tar -cvjf ${PWD}/${TAGNAME}@${UUID}.tar.bz2 ${TAGNAME}@${UUID}.*
#chmod a+w ${PWD}/${TAGNAME}@${UUID}.tar.bz2
#scp ${PWD}/${TAGNAME}@${UUID}.tar.bz2 webcondvm.cern.ch:/tmp
#scp ${PWD}/${TAGNAME}@${UUID}.db webcondvm.cern.ch:/tmp
#scp ${PWD}/${TAGNAME}@${UUID}.txt webcondvm.cern.ch:/tmp
#ssh webcondvm.cern.ch "mv /tmp/${TAGNAME}@${UUID}.tar.bz2 /DropBox"
#ssh webcondvm.cern.ch "mv /tmp/${TAGNAME}@${UUID}.db /DropBox"
#ssh webcondvm.cern.ch "mv /tmp/${TAGNAME}@${UUID}.txt /DropBox"
./upload.py ${TAGNAME}.txt

exit 0

