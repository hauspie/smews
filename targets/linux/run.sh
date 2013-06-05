#!/bin/bash
script_path=`cd \`dirname $0\` && pwd`
smews_path="$script_path/../.."
gksudo bin/linux/smews.elf
