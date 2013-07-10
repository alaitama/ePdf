import os
import pyPdf
from pyPdf import PdfFileReader, PdfFileWriter
from pyPdf.generic import NameObject, createStringObject

import optparse
from optparse import OptionParser

OUTPUT = 'output.pdf'

def getMeta(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    return docInfo;

def printMeta(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print '[*] PDF MetaData For: ' + str(fileName)
    for metaItem in docInfo:
        print '[+] ' + metaItem + ':' + docInfo[metaItem]
        
def modifyMeta(pathFile, fileNameInput, fileNameOutput):
    # There is no interface through pyPDF with which to set this other then getting
    # your hands dirty like so:
    inputFile = os.path.join(pathFile,fileNameInput)
    outputFile = os.path.join(pathFile,fileNameOutput)
    print outputFile
    
    output = PdfFileWriter()
    infoDict = output._info.getObject()
    
    infoDict.update({
        NameObject('/Title'): createStringObject(u'title'),
        NameObject('/Author'): createStringObject(u'author'),
        NameObject('/Subject'): createStringObject(u'subject'),
        NameObject('/Creator'): createStringObject(u'a script'),
        NameObject('/Producer'): createStringObject(u'producer')
    })

    #inputs = [PdfFileReader(i) for i in INPUTS]
    #for input in inputs:
    pdfFile = PdfFileReader(file(inputFile, 'rb'))
    for page in range(pdfFile.getNumPages()):
        output.addPage(pdfFile.getPage(page))

    outputStream = file(outputFile, 'wb')
    output.write(outputStream)
    outputStream.close()
    

def main():
    parser = optparse.OptionParser('usage %prog "+\
    "-F <PDF file name>')
    parser.add_option('-F', dest='fileName', type='string',\
    help='specify PDF file name')
    (options, args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print parser.usage
        exit(0)
    else:
        printMeta(fileName)
        #modifyMeta(fileName)

if __name__ == '__main__':
    main()

