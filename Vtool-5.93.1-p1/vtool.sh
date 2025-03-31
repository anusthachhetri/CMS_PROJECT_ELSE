#!/bin/sh

if [ -z "$VTOOL_DIR" -o ! -d "$VTOOL_DIR" ] ; then
  ## resolve links - $0 may be a link to uctool¡Çs home
  PRG="$0"

  # need this for relative symlinks
  while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \(.*\)$'`
      if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
      else
        PRG=`dirname "$PRG"`"/$link"
      fi
  done

  VTOOL_DIR=`dirname "$PRG"`

  # make it fully qualified
  VTOOL_DIR=`cd "$VTOOL_DIR" && pwd`
fi

java -Xmx1024m -jar  $VTOOL_DIR/vtool.jar "$@"
