#!/usr/bin/python
"""
Popcorn custom builder script.
This script runs Popcorn's Makefile to produce the desired custom build.
"""

import cgi
import sys
import os
import subprocess
import random
import string

# Update the following variables if necessary
pwd = sys.path[0]
popcornDir = pwd + '/popcorn-js'
outputDir = 'dist/custom' # relative to popcornDir
version = '0.5'

# Process input
form = cgi.FieldStorage(keep_blank_values=1)
parts = ()
if form.has_key("parts"):
  parts = form['parts'].value.split(' ')

# Validate input
for i in range(len(parts)):
  # Remove ../
  parts[i] = parts[i].replace('../', '')

  # Check file existance
  if not os.path.exists(popcornDir + '/' + parts[i]):
    print 'Status: 500'
    print 'Content-Type: text/html\n'
    sys.exit(1)

# Get a random file name
def randomString(length):
  str = ''
  for i in range(length):
    str += random.choice(string.letters + string.digits)
  return str

filename = randomString(40)
while os.path.exists(popcornDir + '/' + outputDir + '/' + filename + '.js'):
  filename = randomString(40)

# Make the file now
os.chdir(popcornDir)
if not os.path.exists(outputDir):
  os.makedirs(outputDir)

p = subprocess.call([
    'make',
    'VERSION=' + version,
    'PARTS=' + string.join(parts, ' '),
    'CUSTOM_DIST=' + outputDir + '/' + filename + '.js',
    'CUSTOM_MIN=' + outputDir + '/' + filename + '.min.js',
    'custom'
  ], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print 'Content-Type: text/html\n'
print filename

