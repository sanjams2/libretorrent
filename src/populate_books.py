#!/usr/bin/env python3
import csv
import htmlmin
import xml.etree.ElementTree as et
from urllib.parse import quote

# Constants
BOOK_DATA_PATH = "data/books.csv"
HTML_TEMPLATE_PATH = "html/template.html"
HTML_INDEX_PATH = "html/index.html"
IMAGE_FIELD_NAME = "image_link"
BREAK_MARKER = "BREAKMEUP"

# HTML constants
IMAGE_HEIGHT = str(250)

## Email constants
BODY = """
Hi,

I would like to loan "{title}" by "{author}". My address is:

<PUT YOUR ADDRESS HERE>

Thanks
"""
SUBJECT = "LibreTorrent Book Request"
EMAIL_ADDRESS = "libretorrent.requests@gmail.com"
MAIL_TO_TEMPLATE = "mailto:{}?Subject={}&Body={}".format(quote(EMAIL_ADDRESS), quote(SUBJECT), "{body}")

def get_first_elem(node, *tags):
	if len(tags) == 0:
		return node
	next_node = next(node.iter(tags[0]))
	return get_first_elem(next_node, *tags[1:])

def insert_header(table_node, headers):
	row = et.SubElement(table_node, 'tr')
	et.SubElement(row, 'th') # image
	for header in headers:
		if header != IMAGE_FIELD_NAME:
			et.SubElement(row, 'th').text = header.title()
	et.SubElement(row, 'th') # request link

def insert_row(table_node, headers, book):
	row = et.SubElement(table_node, 'tr')
	image_data = et.SubElement(row, "td")
	et.SubElement(image_data, 'img', {"src": book[IMAGE_FIELD_NAME], "height": IMAGE_HEIGHT})
	for header in headers:
		if header != IMAGE_FIELD_NAME:
			et.SubElement(row, 'td').text = book[header].replace(": ", ":" + BREAK_MARKER) # hack to add line break
	link_data = et.SubElement(row, "td")
	# Assumes a title and author field (seems like a safe assumption)
	body = quote(BODY.format(title=book['title'], author=book['author']))
	et.SubElement(link_data, "a", {"href": MAIL_TO_TEMPLATE.format(body=body)}).text = "Request"

def main():
	with open(BOOK_DATA_PATH) as fh:
		reader = csv.DictReader(fh)
		headers = reader.fieldnames
		books = [row for row in reader]
	tree = et.parse(HTML_TEMPLATE_PATH)
	root = tree.getroot()
	# brittle; assumes 1 table in the first level of the body 
	table = get_first_elem(root, 'body', 'table')
	insert_header(table, headers)
	for book in books:
		insert_row(table, headers, book)
	string_body = et.tostring(root, method="html").decode('utf-8').replace(BREAK_MARKER, "</br>")
	with open(HTML_INDEX_PATH, 'w') as fh:
		fh.write(string_body)

if __name__ == '__main__':
	main()