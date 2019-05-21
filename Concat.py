# Linter PEP8
# Python 3.6.5

import os
import glob
# Program Flow:
# Check for and Store comments
# Store masterHeader, calculate number of fields
# verify csv data against csv field count found from header

# Global Variables
stdDelim = ","
commentDelim = ""
comments = []
dataList = []
masterHeader = ""
headerFound = False
numFields = 0

CommentDebug = False
HeaderDebug = False
DataDebug = False


def parseFile(file):
    global masterHeader
    global comments
    global headerFound

    fileLines = []
    data = []
    line = ""
    output = ""
    # print("\n\nFile:" + file)
    with open(file) as fp:
        fileLines += fp.read().splitlines()
    for line in fileLines:
        line = line.rstrip('\r\n')
        output = parseLine(file, line)
        if(output is not None):
            data.append(output)
    if(DataDebug):
        print("Parse Line Returns: " + str(output) + " " + str(type(output)))
    return data


# Check for 3 possible conditions:
# line is comment
# we have no header: set it
# header is known: line is data
#
# Accepts: line to parse
# Returns: csvdata as string if header has been found
def parseLine(file, line):
    global stdDelim
    global commentDelim
    global comments
    global masterHeader
    global headerFound
    global numFields
    lineData = ""

    line = line.strip()
    # print("Header status:" + str(headerFound))
    # line is comment
    if line.startswith(commentDelim):
        # Append comment to comment list
        comments.append(line)
        # print("Comment Appended, line" + str(line))
        # print("Comment list appears: " + str(comments))

    # we have no header: set it
    # Set Header, compare against Master
    elif headerFound is False:
        # print("setting header")
        header = line
        headerFound = True
        numFields = header.count(stdDelim)
        # print("Header: " + header + " Has " + str(numFields) + " fields")
        if not masterHeader:
            masterHeader = header
            # print("Master Header set: " + masterHeader)
        else:
            if header != masterHeader:
                print("Header Mismatch")
            elif header == masterHeader:
                # print("Header matches master")
                pass
    # header is known: line is data
    # match data against header
    elif headerFound is True and line is not "":
        # print("We already have a Header")
        # nieve check, comma counts are equal
        lineFields = line.count(stdDelim)
        if (lineFields == numFields):
            # print("CSV Data is: " + line)
            lineData = line
            return lineData
        else:
            print(file + " problem, Header: " + str(numFields) +
                  " Fields, row has " + str(lineFields) + " Fields")
            return ("#" + line)
    else:
        print("unreachable")


def writeOut(outfile, comments, masterHeader, dataList):
    # write comments
    with open(outfile, 'w') as f:
        f.write("# Start Comments\n")
        for item in comments:
            f.write("%s\n" % item)
        f.write("# End Comments\n\n")
    # write header
        f.write("# Header\n")
        f.write("%s" % masterHeader)
        f.write("\n# End Header\n")
    # write data
        f.write("\n# Start Data\n")
        for item in dataList:
            f.write("%s\n" % item)
        f.write("# End Data\n\n")


def concat(indir="/home/chris/Documents/Playground/MM/csv/CM4_ATMOS_LEVEL_50101_46k/sample/",
           outfile="/home/chris/Documents/Playground/MM/csv/CM4_ATMOS_LEVEL_50101_46k/output.txt",
           delim=',', comment='#', escaped=['\n', '\a', '\b']):
    global stdDelim
    global commentDelim
    global headerFound
    global dataList
    global numFields

    stdDelim = delim
    commentDelim = comment
    os.chdir(indir)
    fileList = glob.glob("*.csv")

    # iterate each file
    for file in fileList:
        dataList = dataList + parseFile(file)
        # Reset for next file
        headerFound = False
        numFields = 0
    writeOut(outfile, comments, masterHeader, dataList)

concat()
