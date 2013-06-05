#!/bin/bash
SUDO=sudo
test "$1" = "-gui" && SUDO=gksudo
$SUDO pkill smews.elf &
