import fitz # PyMuPDF
import sys
doc = fitz.open("itv.pdf")
page = doc[0] # page 1
pix = page.get_pixmap()
pix.save("itv_page1.png")
