#! /usr/bin/env python
"""
Script to invoke scanning on a twain-compatible printer and to convert 
scanned pages to a PDF. Also includes a routine to easily scan multiple 
pages at once. 
"""

import Tkinter, tkMessageBox, tkFileDialog
from argparse import ArgumentParser
from datetime import datetime
from os import path, remove, pardir
from subprocess import PIPE, STDOUT, Popen
import time

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Invoke GUI
Tkinter.Tk().withdraw()

# Command line arguments
parser = ArgumentParser(description='Scan pages and create PDF.')
parser.add_argument('-r', metavar='<Resolution>', default=100,
                    help='Scan resolution in DPI (100 - 1000).')
parser.add_argument('-c', metavar='<Contrast>', default=0,
                    help='Contrast (-1000 - 1000).')
parser.add_argument('-i', metavar='<Image-Qlt>', default=90,
                    help='Image Quality (10-100).')
parser.add_argument('-k', action='store_true',
                    help='Keep temporary image files', default='False')

args = parser.parse_args()

args.r = int(args.r)
if args.r < 100 or args.r > 1000:
    print 'Value for resolution ({}) invalid.'.format(args.r)
    parser.print_help()
    exit(1)

args.c = int(args.c)
if args.c < -1000 or args.c > 1000:
    print 'Value for contrasts ({}) invalid.'.format(args.c)
    parser.print_help()
    exit(1)

args.i = int(args.i)
if args.i < 10 or args.i > 100:
    print 'Value for jpeg quality ({}) invalid.'.format(args.i)
    parser.print_help()
    exit(1)

print 'SCAN_RES={}; CONTRAST={}; JPEG_Q={}; KEEP_TMP={}'.format(
    args.r, args.c, args.i, args.k)
    
# Get target_filename for final PDF file
default_filename = (datetime.fromtimestamp(
                    time.time()).strftime('%Y-%m-%d') + '-DOCNAME')
file_opt = {}
file_opt['initialdir'] = '.'
file_opt['initialfile'] = default_filename
file_opt['title'] = 'Select location for final PDF file'
file_opt['filetypes'] = [('PDF Files', '.pdf')]
target_filename = tkFileDialog.asksaveasfilename(**file_opt)

if target_filename == '':
    exit()
else:
    if not target_filename.endswith('.pdf'):
        target_filename = target_filename + '.pdf'

target_filename = path.abspath(target_filename)
print 'Target filename will be {0}'.format(target_filename)
target_folder = path.abspath(path.join(target_filename, pardir))
print 'Target folder for temporary files will be {0}'.format(target_folder)

images = []
temp_files = []
workdir = path.join(path.dirname(path.realpath(__file__)),
                        'cmdtwain-win')

# Scan as many pages as the user desires...
while True:
                 
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
    image = path.join(target_folder, timestamp) + '.bmp'
    print 'Creating temporary file at: {0}'.format(image)
    
    
    command = '{} /PAPER=a4 /RGB /DPI={} {}'.format(
                path.join(workdir, 'ScanBmp.exe'), args.r, image)
    
    handle = Popen(command, shell=True, stdout=PIPE,
                              stderr=STDOUT, cwd=workdir)
    handle.wait()
    images.append(image)
    temp_files.append(image)
    
    # Now the temporary image file lies on the file system
    
    result = tkMessageBox.askquestion(title="Basti's scan tool",
                                       message="Scan another page?")
    if result == 'yes':
        pass
    else:
        break

# Take a list of JPG/PNG/BMP images and stores the images to 
# an A4-format PDF with each image as one page
c = canvas.Canvas(target_filename)
c.setPageCompression(1)
for image in images:
    image_jpeg = image + '.jpg'
    temp_files.append(image_jpeg)
    try:
        im = Image.open(image)
        im.save(image_jpeg, 'JPEG', quality=args.i)
    except IOError:
        print 'Cannot create jpeg for {}'.format(image)
    c.drawImage(image_jpeg, 0, 0, 21 * cm, 29.7 * cm)
    c.showPage()
c.save()

if args.k == 'False':
    for temp_file in temp_files:
        if path.exists(temp_file):
            print 'Removing temporary file: {0}'.format(temp_file)
            remove(temp_file)
