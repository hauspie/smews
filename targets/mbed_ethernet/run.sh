#!/bin/bash

set -e


target=mbed_ethernet
script_path=`cd \`dirname $0\` && pwd`
smews_path=$script_path/../../

mbed_path=`mount -l | grep MBED | cut -d\  -f3 | head -1`
cp $smews_path/bin/$target/smews.bin $mbed_path && sync && sleep 1

mbed_tty=`ls /dev/ttyACM? | head -1`
$smews_path/tools/send_break $mbed_tty
