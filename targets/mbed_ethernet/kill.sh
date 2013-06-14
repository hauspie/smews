#!/bin/bash

set -e

script_path=`cd \`dirname $0\` && pwd`
smews_path=$script_path/../../

mbed_path=`mount -l | grep MBED | cut -d\  -f3 | head -1`
dd if=/dev/urandom of=$mbed_path/smews.bin bs=1024 count=1 && sync && sleep 1

mbed_tty=`ls /dev/ttyACM? | head -1`
$smews_path/tools/send_break $mbed_tty
