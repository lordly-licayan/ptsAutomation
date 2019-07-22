#!/bin/sh

workDate=`date '+%Y-%m-%d'`
timestamp=$(date +%s)
workDir=$HOME/robot/output/${workDate}/${timestamp}
robotFilename=$1

echo "Executing file ${robotFilename}..."
mkdir -p $workDir
echo ">>> Created output folder ${workDir}"

robot -T --outputdir ${workDir} ${robotFilename}