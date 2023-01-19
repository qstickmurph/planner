from datetime import date, timedelta
import calendar
import sys
import re
import subprocess
import os
from parse_template import parse_template

_weekdayDict = {
        0 : "Monday",
        1 : "Tuesday",
        2 : "Wednesday",
        3 : "Thursday",
        4 : "Friday",
        5 : "Saturday",
        6 : "Sunday"
        }

_monthDict = {
        1 : "January",
        2 : "Februrary",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10: "October",
        11: "November",
        12: "December"
        }

def _num_suffix(num):
    if num % 10 == 1:
        return "st"
    if num % 10 == 2:
        return "nd"
    if num % 10 == 3:
        return "rd"
    return "th"

# Ask user what template to use
while True:
    templateFolder = input("What template folder would you like to use?")
    templateFolder = "templates/" + templateFolder
    if os.path.isdir(templateFolder):
        break
    else:
        print("Please type a valid folder name inside of ./templates/")

def parse_config(data:str):
    data = data.strip()
    if data == "True":
        return True
    elif data == "False":
        return False
    try:
        return int(data)
    except:
        try:
            return float(data)
        except:
            return data

conf = {}
# Read in default conf file
with open('default.conf', 'r') as defaultConf:
    read = defaultConf.read()
    for line in read.splitlines():
        split = line.split('=')
        conf[split[0]] = parse_config(split[1])

# Read contants from conf.conf
try:
    with open(templateFolder + '/conf.conf', 'r') as confFile:
        read = confFile.read()
        for line in read.splitlines():
            split = line.split('=')
            conf[split[0]] = parse_config(split[1])
except IOError:
    print("No valid conf file in templates/" + templateFolder + ". Resorting to default conf file")

# Ask user for parameters
if conf["includesDates"]:
    while True:                                                                                                                                                                                            
        startDate = input("Start Date (YYYY-MM-DD): ")

        try:
            startDate = date.fromisoformat(startDate)
        except ValueError:
            print("Invalid string")
        else:
            break

    while True:
        endDate = input("End Date (YYYY-MM-DD): ")

        try:
            endDate = date.fromisoformat(endDate)
        except ValueError:
            print("Invalid string")
        else:
            if endDate < startDate:
                print("End Date must follow startDate")
            else:
                break

while True:
    try:
        signatureSize = int(input(f"How many pages per signature? "))
    except TypeError:
        print("Invalid response")
    else:
        break

while True:
    try:
        minEndpages = int(input(f"How many end pages would you like? (minimum) "))
    except TypeError:
        print("Invalid response")
    else:
        break

if not conf.get('baseHeight', False):
    while True:
        try:
            baseHeight = float(input("What is the height of the base paper? (units don't matter) "))
        except TypeError:
            print("Invalid response")
        else:
            break
else:
    baseHeight = conf['baseHeight']

if not conf.get('baseWidth', False):
    while True:
        try:
            baseWidth = float(input("What is the width of the base paper? (units don't matter) "))
        except TypeError:
            print("Invalid response")
        else:
            break
else:
    baseWidth = conf['baseWidth']

# Determine which pages to print

blankFront = input("Include a blank front page? (y/n): ") == "y" if conf['hasBlank'] else False
printTitle = input("Include a title page? (y/n): ") == "y" if conf['hasTitle'] else False
printYearly = input("Print yearly pages? (y/n): ") == "y" if conf['hasYearly'] else False
printQuarterly = input("Print quarterly pages? (y/n): ") == "y" if conf['hasQuarterly'] else False
printMonthly = input("Print monthly pages? (y/n): ") == "y" if conf['hasMonthly'] else False
printWeekly = input("Print weekly pages? (y/n): ") == "y" if conf['hasWeekly'] else False
printDaily = input("Print daily pages? (y/n): ") == "y" if conf['hasDaily'] else False
printEndpages = input("Print endpages? (y/n): ") == "y" if conf['hasEndpage'] else False

if not conf["includesDates"]:
    startDate = date(year=2000,month=1,day=3)
    if printWeekly:
        while True:
            try:
                weeks = int(input("How many weeks would you like to print? "))
                endDate = startDate + timedelta(weeks=weeks) - timedelta(days=1)
            except TypeError:
                print("Invalid response")
            else: 
                break
    else:
        while True:
            try:
                days = int(input("How many days would you like to print? "))
                endDate = startDate + timedelta(days=days-1)
            except TypeError:
                print("Invalid response")
            else: 
                break

# Define the title page parameters
if 'title' not in conf:
    conf['title'] = input("What's the title of the book? ")
if 'subtitle' not in conf:
    conf['subtitle'] = input("What's the subtitle of the book? (optional) ")
if 'ownerName' not in conf:
    conf['ownerName'] = input("What's the name of the owner of the book? ")
if 'phoneNumber' not in conf:
    conf['phoneNumber'] = input("What's their phone #? ")
if 'address1' not in conf:
    conf['address1'] = input("What's the first line of their street address? ")
if 'address2' not in conf:
    conf['address2'] = input("What's the second line of their street address? (optional) ")
if 'city' not in conf:
    conf['city'] = input("What city do they live in? ")
if 'state' not in conf:
    conf['state'] = input("What state do they live in? ")
if 'country' not in conf:
    conf['country'] = input("What country do they live in? ")
if 'zipCode' not in conf:
    conf['zipCode'] = input("What's their postal code? ")

print("Creating / writing to output_planner.tex")
# Write output_planner.tex file
output = open("tex/output_planner.tex", "w+")

# Document Class
output.write("\\documentclass[tikz]{standalone}\n\n")

# Load Packages
output.write("\\usepackage{lmodern}\n"
        + "\\usepackage{tikz}\n"
        + "\t\\usetikzlibrary{positioning}\n\n")

# Begin Document
output.write("\\begin{document}\n")

numPages = 0

## Print Blank Pages
if blankFront:
    output.write(parse_template(templateFolder, "blank"))
    numPages += conf['pagesBlank']

# Print Title Page
if printTitle:
    output.write(parse_template(templateFolder, "title", **conf))
    numPages += conf['pagesTitle']

# Change startDate and endDate to fit into time chunks desired
if printYearly: 
    startDate = startDate.replace(month=1, day=1)
    endDate = endDate.replace(month=12, day=31)
if printQuarterly: 
    newStartMonth = (startDate.month - 1 - (startDate.month - 1) % 3) % 12 + 1
    startDate = startDate.replace(month=newStartMonth, day=1)
    newEndMonth = (endDate.month - 1 - (endDate.month - 1) % 3 + 2) % 12 + 1
    endDate = endDate.replace(month=newEndMonth, day=calendar.monthrange(endDate.year, newEndMonth)[1])
if printMonthly: 
    startDate = startDate.replace(day=1)
    endDate = endDate.replace(day=calendar.monthrange(endDate.year, endDate.month)[1])
if printWeekly: 
    startDate = startDate - timedelta(days=startDate.weekday())
    endDate = endDate + timedelta(days=6-endDate.weekday())

# Then, print each day's pages until we've reached the end
while(startDate <= endDate):
    # Evaluate what pages will be printed this step
    d = True
    w = d and startDate.weekday() == 0
    m = w and (startDate + timedelta(days=6)).day <= 7 and (startDate + timedelta(days=6)) < endDate
    q = m and ((startDate + timedelta(days=6)).month - 1) % 3 == 0
    y = q and (startDate + timedelta(days=6)).month == 1

    # Change date based conf vars
    conf['date'] = startDate
    conf['dayNum'] = startDate.day
    conf['day'] = _weekdayDict[startDate.weekday()]
    conf['daySuffix'] = _num_suffix(startDate.day)
    conf['monthNum'] = startDate.month
    conf['month'] = _monthDict[startDate.month]
    conf['year'] = startDate.year
    conf['endOfWeekDayNum'] = (startDate + timedelta(days=6)).day
    conf['endOfWeekDay'] = _weekdayDict[(startDate + timedelta(days=6)).weekday()]
    conf['endOfWeekDaySuffix'] = _num_suffix((startDate + timedelta(days=6)).day)
    conf['endOfWeekMonthNum'] = (startDate + timedelta(days=6)).month
    conf['endOfWeekMonth'] = _monthDict[(startDate + timedelta(days=6)).month]
    conf['endOfWeekYear'] = (startDate + timedelta(days=6)).year
    
    # Print them
    if printYearly and y:
        output.write(parse_template(templateFolder, "year", **conf))
        numPages += conf['pagesYearly']
    if printQuarterly and q:
        output.write(parse_template(templateFolder, "quarter", **conf))
        numPages += conf['pagesQuarterly']
    if printMonthly and m:
        output.write(parse_template(templateFolder, "month", **conf))
        numPages += conf['pagesMonthly']
    if printWeekly and w:
        output.write(parse_template(templateFolder, "week", **conf))
        numPages += conf['pagesWeekly']
    if printDaily and d:
        output.write(parse_template(templateFolder, "day", **conf))
        numPages += conf['pagesDaily']

    startDate += timedelta(days=1)

# print endpages
if printEndpages:
    endpage = parse_template(templateFolder, "endpage", **conf)
    numEndpages = 0
    while numEndpages < minEndpages or numPages % signatureSize != 0:
        output.write(endpage)
        numEndpages += conf['pagesEndpage']
        numPages += conf['pagesEndpage']

# Finish the document and close the file
output.write("\\end{document}\n")
print("Closing output_planner.tex")
output.close()

# Create first pdf from vanilla tex
print("Creating output_planner.pdf")
subprocess.run(['pdflatex', '-output-directory=output', 'tex/output_planner.tex'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)

depth = 1
while 2 ** (depth) < conf['pagesPerSheet']:
    print(f"Creating signatures{depth}.tex")
    signatures = open(f'tex/signatures{depth}.tex', 'w+')
    signatures.write("\\documentclass{article}\n"
#            + f"\\usepackage[paperheight={baseHeight}in, paperwidth={baseWidth}in]{{geometry}}\n"
            + f"\\usepackage[paperheight={baseHeight if depth%2 == 0 else 2*baseWidth}in, paperwidth={baseWidth if depth%2 == 0 else baseHeight}in]{{geometry}}\n"
            + "\\usepackage{pdfpages}\n\n"
            + "\\begin{document}\n")
    if depth == 1:
        signatures.write(f"\t\\includepdf[pages=-, signature={str(2*signatureSize // 2**(depth))},landscape]{{output/output_planner.pdf}}\n")
    else:
        signatures.write(f"\t\\includepdf[pages=-, signature={str(2*signatureSize // 2**(depth))},landscape]{{output/signatures{depth-1}.pdf}}\n")
    signatures.write("\\end{document}")
    signatures.close()
    
    print(f"Creating signatures{depth}.pdf")
    subprocess.run(['pdflatex', '-output-directory=output', f'tex/signatures{depth}.tex'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

    depth += 1

print(f"Final output written on signatures{depth-1}.pdf")