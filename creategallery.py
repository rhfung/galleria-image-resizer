# Copyright (C) 2013, Richard H Fung
# http://www.rhfung.com 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Usage:
#  python creategallery.py <base-directory>
#
# The base directory should contain .JPG images that will be shown in the gallery.
#

import os
import sys
from fnmatch import fnmatch
import Image
import string

def generate_and_save_thumbnail(imageFile, counter, w, h):
	image = Image.open(imageFile)
	image.thumbnail((w, h), Image.ANTIALIAS)
	outFileLocation = os.path.dirname(imageFile) + "/thumbnails/"
	outFileName = "thumb" + str(counter) + "_" + os.path.splitext(os.path.basename(imageFile) )[0]
	image.save(outFileLocation + outFileName + ".jpg", "JPEG")
	return outFileLocation + outFileName + ".jpg"
	
def resize_and_save_thumbnail(imageFile, counter, w, h):
	image = Image.open(imageFile)
	image.thumbnail((w, h), Image.ANTIALIAS)
	outFileLocation = os.path.dirname(imageFile) + "/images/"
	outFileName = "photo" + str(counter) + "_" + os.path.splitext(os.path.basename(imageFile) )[0]
	image.save(outFileLocation + outFileName + ".jpg", "JPEG")
	return outFileLocation + outFileName + ".jpg"


	# Windows - getctime (creation), UNIX - getmtime (modification)
def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a
	
relativeBasePath = sys.argv[1]
filelist = getfiles(relativeBasePath)
counter = 0

if not os.path.exists(relativeBasePath + "/thumbnails"):
	os.mkdir(relativeBasePath + "/thumbnails")

if not os.path.exists(relativeBasePath + "/images"):
	os.mkdir(relativeBasePath + "/images")

template_dir = os.path.dirname(os.path.realpath(__file__))

f = open(template_dir + "/creategallery-template.html")
template_file = f.read()
f.close()

insert_contents = ""


for file in filelist:
	if fnmatch(file, "*.jpg") or fnmatch(file, "*.png"):
		filePath = sys.argv[1] + "/" + file
		thumbnailFilePath = generate_and_save_thumbnail(filePath, counter, 93, 70)
		resizedFilePath = resize_and_save_thumbnail(filePath,  counter, 3000, 2250)
		insert_contents = insert_contents + '<a href="' + resizedFilePath + '"><img src="' + thumbnailFilePath + '"></a>\n'
		counter = counter + 1


print string.replace(template_file, "{{contents}}", insert_contents)
