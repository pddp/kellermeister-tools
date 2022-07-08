.phony: dump

dump	:
	export D=$$(date '+%y%m%d'); mysqldump -u paulus -p Weinkeller > Weinkeller$$D.sql

sed	: 
	sed -e 's/),(/);\nINSERT INTO `Lagerung` VALUES (/g'

pretty	:

storages.new : storages.xml jacques.py Makefile
	xmllint --format storages.xml > storages.bak
	cp storages.bak storages.xml
	- rm -f storages.tmp
	ipython jacques.py 
	awk '/<?xml/,/<storage name=/' < storages.bak | head -n -1 > storages.out
	cat storages.tmp >> storages.out
	tail -2 storages.xml >> storages.out
	xmllint --format storages.out > storages.new


