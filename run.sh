#!/bin/bash - 
#===============================================================================
#
#          FILE:  run.sh
# 
#         USAGE:  ./run.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: YOUR NAME (), 
#       COMPANY: 
#       CREATED: 06/08/2013 13:26:44 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

rm *.dot
rm dot*.png

nosetests -s

for dfile in *.dot
do
    dot $dfile -Tpng > dot${dfile%%dot}png
done

open dot*.png
