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


def convert_images_to_a4_pdf (images, target_pdf='output.pdf'):  
    """Takes a list of JPG/PNG/BMP images and stores the images to 
       an A4-format PDF with each image as one page."""
       
    c = canvas.Canvas(target_pdf)
    c.setPageCompression(1)
    for image in images:
        c.drawImage(image, 0, 0, 21 * cm, 29.7 * cm)
        c.showPage()
    c.save()
    

def scan_image (target_file, resolution=100, contrast=0):
    """Uses a twain-compatible scanner to scan an image to BMP"""
    
    workdir = path.join(path.dirname(path.realpath(__file__)),
                        'cmdtwain-win')
    command = '{} /PAPER=a4 /RGB /DPI={} {}'.format(
                path.join(workdir, 'ScanBmp.exe'), resolution, target_file)
    
    handle = Popen(command, shell=True, stdout=PIPE,
                              stderr=STDOUT, cwd=workdir)
    handle.wait()

Tkinter.Tk().withdraw()

# Command line arguments
parser = ArgumentParser(description='Scan pages and create PDF.')
parser.add_argument('-r', metavar='<Resoultion>', default=100,
                    help='Scan resoultion in DPI (> 100).')
parser.add_argument('-c', metavar='<Contrast>', default=0,
                    help='Contrast (-1000 - 1000).')
parser.add_argument('-keeptemp', action='store_true',
                    help='Keep temporary image files', default='False')

args = parser.parse_args()
    
# Get target_filename for final PDF file
default_filename = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') + '-DOCNAME'
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

# Scan as many pages as the user desires...
while True:
                 
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
    image = path.join(target_folder, timestamp) + '.bmp'
    print 'Creating temporary file at: {0}'.format(image)
    
    scan_image (image, args.r, args.c)
    images.append(image)
    
    # Now the temporary image file lies on the file system
    
    result = tkMessageBox.askquestion(title="Basti's scan tool",
                                       message="Scan another page?")
    if result == 'yes':
        pass
    else:
        break

convert_images_to_a4_pdf(images, target_filename)

if args.keeptemp == 'False':
    for temp_file in images:
        if path.exists(temp_file):
            print 'Removing temporary file: {0}'.format(temp_file)
            remove(temp_file)
