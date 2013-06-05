#!/bin/bash
script_path=`cd \`dirname $0\` && pwd`
smews_path=$script_path/../../
gksudo $smews_path/bin/linux/smews.elf &
cpt=1
while [ $cpt -ne 10 ]
do
    pgrep smews.elf && exit 0
    cpt=`expr $cpt + 1`
    sleep 1
done
exit 1
