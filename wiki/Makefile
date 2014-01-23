help:
	@echo " "
	@echo "Type ...................      To ................"
	@echo "make all                         everything"
	@echo "make lite                        ignore commented contents"
	@echo " "
all:
	tigernotes doc *.notes -o pyPedLibWiki.pdf --toc --footnote --font_size 11 
lite:
	tigernotes doc *.notes -o pyPedLibWiki.pdf --toc --footnote --font_size 11 --lite
