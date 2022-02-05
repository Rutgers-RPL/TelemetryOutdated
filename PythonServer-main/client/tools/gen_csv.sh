#!/bin/bash
echo $1
echo $2
cp $1 $2
# example usage

sed -i '1s/^/magic,time,latitude,longitude,altitude,accx,accy,accz,mA,V,temp,pressure,checksum\n/' $2 
sed -i 's/ /,/g' $2