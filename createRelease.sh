#!/bin/sh
# TODO: Add version from latest git tag
VERSION=0.1
ROOT=`pwd`
rm -rf ./releases/tmp/
mkdir ./releases/${VERSION}
mkdir -p ./releases/tmp/plugin.video.moontv.fi/resources/language/English
mkdir -p ./releases/tmp/plugin.video.moontv.fi/resources/language/Finnish
mkdir -p ./releases/tmp/plugin.video.moontv.fi/resources/lib

cp ./addon.py ./releases/tmp/plugin.video.moontv.fi
cp ./addon.xml ./releases/tmp/plugin.video.moontv.fi
cp ./changelog.txt ./releases/tmp/plugin.video.moontv.fi
cp ./fanart.png ./releases/tmp/plugin.video.moontv.fi
cp ./icon.png ./releases/tmp/plugin.video.moontv.fi
cp ./LICENSE.txt ./releases/tmp/plugin.video.moontv.fi
cp ./README.md ./releases/tmp/plugin.video.moontv.fi
cp ./resources/__init__.py ./releases/tmp/plugin.video.moontv.fi/resources/
cp ./resources/language/English/strings.xml ./releases/tmp/plugin.video.moontv.fi/resources/language/English
cp ./resources/language/Finnish/strings.xml ./releases/tmp/plugin.video.moontv.fi/resources/language/Finnish
cp ./resources/lib/__init__.py ./releases/tmp/plugin.video.moontv.fi/resources/lib
cd releases/tmp/
zip -r ../${VERSION}/plugin.video.moontv.fi-${VERSION}.zip plugin.video.moontv.fi/*
cp ${ROOT}/changelog.txt ../${VERSION}/changelog-${VERSION}.txt 
## http://wiki.xbmc.org/index.php?title=Add-on_repositories is not very clear
## of image formats so in future, this might be changed .. 
cp ${ROOT}/fanart.png ../${VERSION}/
cp ${ROOT}/icon.png ../${VERSION}/
