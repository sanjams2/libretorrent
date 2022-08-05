
build:
	python3 src/populate_books.py

upload:
	aws --profile libretorrent s3 cp html/index.html s3://libretorrent.com/index.html

# only works on mac
local: build
	open html/index.html

release: build upload