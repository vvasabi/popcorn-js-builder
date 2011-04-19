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
target = 'custom'
downloadFilename = 'popcorn-' + version

# Process input
form = cgi.FieldStorage(keep_blank_values=1)
parts = []
if form.has_key('parts[]'):
  rawValues = form['parts[]']
  if type(rawValues) == list:
    for i in range(len(rawValues)):
      parts.append(rawValues[i].value)
  else:
    parts.append(rawValues.value)

minify = False
if form.has_key('minify'):
  minify = True
  target = 'custom-min'

# See if there are any parts chosen
if len(parts) == 0:
  print 'Content-Type: text/html\n'
  print 'Nothing to be done...'
  sys.exit(0)

# Validate input
for i in range(len(parts)):
  # Remove ../
  parts[i] = parts[i].replace('../', '')

  # Check file existance
  if not os.path.exists(popcornDir + '/' + parts[i]):
    print 'Status: 500'
    print 'Content-Type: text/html\n'
    print 'A system error occurred. Please try again later.'
    sys.exit(1)

# Get a random file name
def randomString(length):
  str = ''
  for i in range(length):
    str += random.choice(string.letters + string.digits)
  return str

token = randomString(40)
while os.path.exists(popcornDir + '/' + outputDir + '/' + token + '.js'):
  token = randomString(40)

# Make the file now
os.chdir(popcornDir)
if not os.path.exists(outputDir):
  os.makedirs(outputDir)

subprocess.call([
    'make',
    'VERSION=' + version,
    'PARTS=' + string.join(parts, ' '),
    'CUSTOM_DIST=' + outputDir + '/' + token + '.js',
    'CUSTOM_MIN=' + outputDir + '/' + token + '.min.js',
    target
  ], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Read file
path = outputDir + '/' + token + '.js'
if minify:
  path = outputDir + '/' + token + '.min.js'

file = open(path, 'r')
size = os.path.getsize(path)

# Send filedownload
if minify:
  downloadFilename += '.min.js'
else:
  downloadFilename += '.js'

print 'Content-Type: text/javascript;'
print 'Content-Disposition: attachment; filename="%s"' % downloadFilename
print 'Content-Length: %d\n' % size
print file.read()
file.close()

# Clean up
os.remove(outputDir + '/' + token + '.js')
if minify:
  os.remove(outputDir + '/' + token + '.min.js')

