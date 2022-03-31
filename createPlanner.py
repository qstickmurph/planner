from datetime import date, timedelta
import calendar
import sys
import re
import subprocess
import os
import halfPages
import quarterPages

# Ask user for parameters
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
    pagesPerSheet  = int(input("Would you like a (2) half-sized or (4) quarter-sized booklet? "))
    if pagesPerSheet == 2: #half sized booklet
        pageClass = halfPages
        break

    elif pagesPerSheet == 4: # quarter sized bookley
        pageClass = quarterPages
        break
        
    else:
        print("Please enter a valid entry")

while True:
    try:
        signatureSize = int(input(f"How many sheets per signature? "))
    except TypeError:
        print("Invalid response")
    else:
        break

printYearly = input("Print yearly pages? (y/n): ") == "y"
printQuarterly = input("Print quarterly pages? (y/n): ") == "y"
printMonthly = input("Print monthly pages? (y/n): ") == "y"
printWeekly = input("Print weekly pages? (y/n): ") == "y"
printDaily = input("Print daily pages? (y/n): ") == "y"
title = input("What's the title of the book? ")
subtitle = input("What's the subtitle of the book? (optional) ")
ownerName = input("What's the name of the owner of the book? ")
phoneNumber = input("What's their phone #? ")
address1 = input("What's the first line of their street address? ")
address2 = input("What's the second line of their street address? (optional) ")
city = input("What city do they live in? ")
state = input("What state do they live in? ")
country = input("What country do they live in? ")
zipCode = input("What's their postal code? ")

print("Creating / writing to output_planner.tex")
# Write output_planner.tex file
output = open("output_planner.tex", "w+")

# Document Class
output.write("\\documentclass[tikz]{standalone}\n\n")

# Load Packages
output.write("\\usepackage{lmodern}\n"
        + "\\usepackage{tikz}\n"
        + "\t\\usetikzlibrary{positioning}\n\n")

# Begin Document
output.write("\\begin{document}\n")

# Print Title Page
pageClass.print_title(output, title, subtitle, ownerName, phoneNumber, address1, address2, city, state, country, zipCode)

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
    
    # Print them
    if printYearly and y:
        pageClass.print_year(output, startDate + timedelta(days=6))
    if printQuarterly and q:
        pageClass.print_quarter(output, startDate + timedelta(days=6))
    if printMonthly and m:
        pageClass.print_month(output, startDate + timedelta(days=6))
    if printWeekly and w:
        pageClass.print_week(output, startDate)
    if printDaily and d:
        pageClass.print_day(output, startDate)

    startDate += timedelta(days=1)

# Finish the document and close the file
output.write("\\end{document}\n")
print("Closing output_planner.tex")
output.close()

# Create first pdf from vanilla tex
print("Creating output_planner.pdf")
subprocess.run(['pdflatex', 'output_planner.tex'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)

depth = 0
while 2 ** (depth) < pagesPerSheet:
    print(f"Creating signatures{depth}.tex")
    signatures = open(f'signatures{depth}.tex', 'w+')
    signatures.write("\\documentclass{article}\n"
            + f"\\usepackage[paperheight={pageClass.paper_height(depth)}, paperwidth={pageClass.paper_width(depth)}]{{geometry}}\n"
            + "\\usepackage{pdfpages}\n\n"
            + "\\begin{document}\n")
    if depth == 0:
        signatures.write(f"\t\\includepdf[pages=-, signature={str(signatureSize * pagesPerSheet // 2**(depth))},landscape]{{output_planner.pdf}}\n")
    else:
        signatures.write(f"\t\\includepdf[pages=-, signature={str(signatureSize * pagesPerSheet // 2**(depth))},landscape]{{signatures{depth-1}.pdf}}\n")
    signatures.write("\\end{document}")
    signatures.close()
    
    print(f"Creating signatures{depth}.pdf")
    subprocess.run(['pdflatex', f'signatures{depth}.tex'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

    depth += 1

print(f"Final output written on signatures{depth-1}.pdf")
