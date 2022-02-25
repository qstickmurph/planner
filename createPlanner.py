from datetime import date, timedelta
import calendar
import sys
import re

weekdayDict = {
        0 : "Monday",
        1 : "Tuesday",
        2 : "Wednesday",
        3 : "Thursday",
        4 : "Friday",
        5 : "Saturday",
        6 : "Sunday"
        }

monthDict = {
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

# Page Functions
def num_suffix(num):
    if num % 10 == 1:
        return "st"
    if num % 10 == 2:
        return "nd"
    if num % 10 == 3:
        return "rd"
    return "th"

def printYear(output, currDate):
    output.write(f"Print Year ({currDate.year})\n")

def printQuarter(output, currDate):
    output.write(f"  Print Quarter ({currDate.year} Quarter {(currDate.month + 2) // 3 })\n")

def printMonth(output, currDate):
    output.write(f"    Print Month ({currDate.year} Month {currDate.month})\n")

def printWeek(output, currDate):
    output.write("\\begin{tikzpicture}[\n"
            + "\tinner sep=3 pt,\n"
            + "\ttitle/.style={%\n"
            + "\t\tnode font=\\Large,\n"
            + "\t},\n"
            + "\tsubtitle/.style={%\n"
            + "\t\tanchor = west,\n"
            + "\t\tnode font=\\large,\n"
            + "\t},\n"
            + "\tday/.style={%\n"
            + "\t\tanchor = west,\n"
            + "\t\tnode font=\\normalsize,\n"
            + "\t},\n"
            + "\thabitdate/.style={%\n"
            + "\t\tanchor = north west,\n"
            + "\t\tnode font = \\footnotesize,\n"
            + "\t},\n"
            + "\thabit/.style={\n"
            + "\t\tanchor = north west,\n"
            + "\t\tnode font = \\footnotesize,\n"
            + "\t},\n"
            + "\tyscale = -1]\n"
            + "\t% Framing Nodes\n"
            + "\t\\node at (0,0) {};\n"
            + "\t\\node at (11,17) {};\n"
            + "\n"
            + "\t% ToDo list lines\n"
            + "\t\\foreach \\i in {1.5, 2, ..., 10.5}{\n"
            + "\t\t\\draw [gray, thin] (1, \\i) -- (5.25, \\i);\n"
            + "\t}\n"
            + "\t% Check Boxes\n"
            + "\t\\foreach \\i in {1, 1.5, ..., 10}{\n"
            + "\t\t\\draw (0.6,\\i+.1) rectangle (0.9,\\i+0.4);\n"
            + "\t}\n"
            + "\n"
            + "\t% Meal Plan Separator\n"
            + "\t\\draw [thick] (0.5, 10.5) -- (10.5, 10.5);\n"
            + "\n"
            + "\t% Meal Plan Day Lines\n"
            + "\t\\foreach \\i in {11.25, 12, ..., 16.5}{\n"
            + "\t\t\\draw (0.5, \\i) -- (5.5, \\i);\n"
            + "\t}\n"
            + "\t\\node [subtitle] at (1.9, 10.9) {Meal Plan};\n"
            + "\t\\node [day] at (0.5, 11.65) {M:};\n"
            + "\t\\node [day] at (0.5, 12.40) {T:};\n"
            + "\t\\node [day] at (0.5, 13.15) {W:};\n"
            + "\t\\node [day] at (0.5, 13.90) {R:};\n"
            + "\t\\node [day] at (0.5, 14.65) {F:};\n"
            + "\t\\node [day] at (0.5, 15.40) {S:};\n"
            + "\t\\node [day] at (0.5, 16.15) {S:};\n"
            + "\n"
            + "\t% Notes section\n"
            + "\t\\node [subtitle] at (7.4, 1.4) {Notes};\n"
            + "\t\\foreach \\i in {1.76, 2.14, ..., 10.5}{\n"
            + "\t\t\\draw [gray, thin] (5.5, \\i) -- (10.5, \\i);\n"
            + "\t}\n"
            + "\n"
            + "\t% Habits Section\n"
            + "\t% Vertical\n"
            + "\t\\foreach \\i in {7.5, 7.875, ..., 10.5}{\n"
            + "\t\t\\draw  [gray, thin] (\\i, 10.5) -- (\\i, 16.5);\n"
            + "\t}\n"
            + "\t\\draw (7.5, 10.5) -- (7.5, 16.5);\n"
            + "\n"
            + "\t% Horizontal\n"
            + "\t\\foreach \\i in {11, 11.5, ..., 16.5}{\n"
            + "\t\t\\draw (5.5, \\i) -- (10.5, \\i);\n"
            + "\t}\n"
            + "\t\\draw [thick] (5.5, 11) -- (10.5,11);\n"
            + "\n"
            + "\t% Text\n"
            + "\t\\node [anchor=north west] at (5.5, 10.52) {Habit};\n"
            + "\t\\node [habitdate] at (7.43, 10.55) {M};\n"
            + "\t\\node [habitdate] at (7.835, 10.55) {T};\n"
            + "\t\\node [habitdate] at (8.16, 10.55) {W};\n"
            + "\t\\node [habitdate] at (8.58, 10.55) {R};\n"
            + "\t\\node [habitdate] at (8.975, 10.55) {F};\n"
            + "\t\\node [habitdate] at (9.36, 10.55) {S};\n"
            + "\t\\node [habitdate] at (9.74, 10.55) {S};\n"
            + "\t\\node [habitdate] at (10.07, 10.52) {\\#};\n"
            + "\n"
            + "\t\\node [habit] at (5.5, 11.05) {Exercise};\n"
            + "\t\\node [habit] at (5.5, 11.55) {Sleep 11-8};\n"
            + "\t\\node [habit] at (5.5, 12.05) {Pets};\n"
            + "\t\\node [habit] at (5.5, 12.55) {Read};\n"
            + "\t\\node [habit] at (5.5, 13.05) {Meditate};\n"
            + "\t\\node [habit] at (5.5, 13.55) {Vit./Meds.};\n"
            + "\t\\node [habit] at (5.5, 14.05) {Eat Healthy};\n"
            + "\n"
            + "\t\\node [habit] at (10.125, 11.05) {5};\n"
            + "\t\\node [habit] at (10.125, 11.55) {7};\n"
            + "\t\\node [habit] at (10.125, 12.05) {7};\n"
            + "\t\\node [habit] at (10.125, 12.55) {7};\n"
            + "\t\\node [habit] at (10.125, 13.05) {7};\n"
            + "\t\\node [habit] at (10.125, 13.55) {7};\n"
            + "\t\\node [habit] at (10.125, 14.05) {6};\n"
            + "\n"
            + "\t% Vertical Split\n"
            + "\t\\draw [thick] (5.5,1) -- (5.5, 16.5);\n"
            + "\n"
            + "\t% Date / Title and Border Lines\n"
            + f"\t\\node at (0.5,0.4) [title] [anchor=north west] {{ Week of {monthDict[currDate.month]} {currDate.day}{num_suffix(currDate.day)}"
                + f" - {monthDict[(currDate + timedelta(days=6)).month]+' ' if (currDate + timedelta(days=6)).month != currDate.month else ''}"
                + f"{(currDate + timedelta(days=6)).day}{num_suffix((currDate + timedelta(days=6)).day)}, {(currDate + timedelta(days=6)).year}}};\n"
            + "\t\\draw [thick] (0.5,1) -- (10.5,1);\n"
            + "\t\\draw [thick] (0.5, 16.5) -- (10.5, 16.5);\n"
            + "\t\\draw [thick] (0.5, 1) -- (0.5, 16.5);\n"
            + "\t\\draw [thick] (10.5, 1) -- (10.5, 16.5);\n"
            + "\n"
            + "\\end{tikzpicture}\n"
            + "\\begin{tikzpicture}[\n"
            + "\tinner sep=3 pt,\n"
            + "\ttitle/.style={%\n"
            + "\t\tnode font=\\Large,\n"
            + "\t},\n"
            + "\tday/.style={%\n"
            + "\t\tanchor=west,\n"
            + "\t\tnode font=\\small,\n"
            + "\t},\n"
            + "\tdate/.style={%\n"
            + "\t\tanchor = east,\n"
            + "\t\tnode font=\\scriptsize,\n"
            + "\t\tcolor=gray,\n"
            + "\t},\n"
            + "\tyscale = -1]\n"
            + "\t% Framing Nodes\n"
            + "\t\\node at (0,0) {};\n"
            + "\t\\node at (11,17) {};\n"
            + "\n"
            + "\t% Minor Horizontal Lines\n"
            + "\t\\foreach \\i in {1.5, 2, ..., 16}{\n"
            + "\t\t\\draw [gray, thin] (0.75, \\i) -- (3.58333, \\i);\n"
            + "\t\t\\draw [gray, thin] (4.08333, \\i) -- (6.91666, \\i);\n"
            + "\t\t\\draw [gray, thin] (7.41666, \\i) -- (10.25, \\i);\n"
            + "\n"
            + "\t}\n"
            + "\n"
            + "\n"
            + "\t% Date / Title and Border Lines\n"
            + "\t\\node at (0.5,0.4) [title] [anchor=north west] {Events, Appointments, and Due Dates};\n"
            + "\t\\draw [thick] (0.5,1) -- (10.5,1);\n"
            + "\t\\draw [thick] (0.5, 16.5) -- (10.5, 16.5);\n"
            + "\t\\draw [thick] (0.5, 1) -- (0.5, 16.5);\n"
            + "\t\\draw [thick] (10.5, 1) -- (10.5, 16.5);\n"
            + "\t\\draw [thick] (0.5, 8.5) -- (10.5, 8.5);\n"
            + "\t\\draw [thick] (7.16666, 12.5) -- (10.5, 12.5);\n"
            + "\n"
            + "\t% Major Horizontal Lines\n"
            + "\t\\draw (0.5, 1.5) -- (10.5, 1.5);\n"
            + "\t\\draw (0.5, 9) -- (10.5, 9);\n"
            + "\t\\draw (7.16666, 13) -- (10.5, 13);\n"
            + "\n"
            + "\t% Days / Dates\n"
            + "\t\\node [day] at (0.5, 1.28) {Monday};\n"
            + "\t\\node [day] at (3.83333, 1.28) {Tuesday};\n"
            + "\t\\node [day] at (7.16666, 1.28) {Wednesday};\n"
            + "\t\\node [day] at (0.5, 8.78) {Thursday};\n"
            + "\t\\node [day] at (3.83333, 8.78) {Friday};\n"
            + "\t\\node [day] at (7.16666, 8.78) {Saturday};\n"
            + "\t\\node [day] at (7.16666, 12.78) {Sunday};\n"
            + "\n"
            + f"\t\\node [date] at (3.83333, 1.28) {{{currDate.strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (7.16666, 1.28) {{{(currDate + timedelta(days=1)).strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (10.5, 1.28) {{{(currDate + timedelta(days=2)).strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (3.83333, 8.78) {{{(currDate + timedelta(days=3)).strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (7.16666, 8.78) {{{(currDate + timedelta(days=4)).strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (10.5, 8.78) {{{(currDate + timedelta(days=5)).strftime('%m/%d')}}};\n"
            + f"\t\\node [date] at (10.5, 12.78) {{{(currDate + timedelta(days=6)).strftime('%m/%d')}}};\n"
            + "\n"
            + "\t% Vertical Lines\n"
            + "\t\\foreach \\i in {0.5, 3.83333, ..., 10.5}{\n"
            + "\t\t\\draw [thick] (\\i, 1) -- (\\i, 16.5);\n"
            + "\t}\n"
            + "\\end{tikzpicture}\n")

def printDay(output, currDate):
    output.write("\\begin{tikzpicture}[\n"
            + "\tinner sep=3 pt,\n"
            + "\ttitle/.style={%\n"
            + "\t\tnode font=\\Large,\n"
            + "\t},\n"
            + "\thournumber/.style={%\n"
            + "\t\tanchor = west,\n"
            + "\t\tnode font=\\small,\n"
            + "\t},\n"
            + "\tminutenumber/.style={%\n"
            + "\t\tanchor = west,\n"
            + "\t\tnode font=\\tiny,\n"
            + "\t\tcolor=gray,\n"
            + "\t},\n"
            + "\tyscale = -1]\n"
            + "\t% Framing Nodes\n"
            + "\t\\node at (0,0) {};\n"
            + "\t\\node at (11,17) {};\n"
            + "\t\n"
            + "\t% Date / Title and Border Lines\n"
            + f"\t\\node at (0.5,0.4) [title] [anchor=north west] {{{weekdayDict[currDate.weekday()]}, {monthDict[currDate.month]} {currDate.day}{num_suffix(currDate.day)} {currDate.year}}};\n"
            + "\t\\draw [thick] (0.5,1) -- (10.5,1);\n"
            + "\t\\draw [thick] (0.5, 16.5) -- (10.5, 16.5);\n"
            + "\t\\draw [thick] (0.5, 1) -- (0.5, 16.5);\n"
            + "\t\\draw [thick] (10.5, 1) -- (10.5, 16.5);\n"
            + "\n"
            + "\t% Hour Numbers\n"
            + "\t\\foreach \\i in {0, 1, ..., 11}{\n"
            + "\t\t\\node [hournumber] at (0.5, \\i*15.5/12 + 1.3) {\\i};\n"
            + "\t}\n"
            + "\t\n"
            + "\t% Minute Numbers\n"
            + "\t\\foreach \\i in {0, 1, ..., 11}{\n"
            + "\t\t\\node [minutenumber] at (0.5, \\i*15.5/12 + 2) {:30};\n"
            + "\t}\n"
            + "\n"
            + "\t% Vertical Lines\n"
            + "\t\\draw (1,1) -- (1, 16.5);\n"
            + "\t\\foreach \\i in {1, 4.16673, ..., 10.5}{\n"
            + "\t\t\\draw (\\i, 1) -- (\\i, 16.5);\n"
            + "\t}\n"
            + "\n"
            + "\t% Minor Horizontal Lines\n"
            + "\t\\foreach \\i in {0.5, 1.5, ..., 11.5}{\n"
            + "\t\t\\draw [gray, thin] (1, \\i*15.5/12 + 1) -- (10.5, \\i*15.5/12 + 1);\n"
            + "\t}\n"
            + "\n"
            + "\t% Major Horizontal Lines\n"
            + "\t\\foreach \\i in {0, 1, ..., 11}{\n"
            + "\t\t\\draw (0.5, \\i*15.5/12 + 1) -- (10.5, \\i*15.5/12 + 1);\n"
            + "\t}\n"
            + "\t\n"
            + "\\end{tikzpicture}\n"
            + "\t\\begin{tikzpicture}[\n"
            + "\tinner sep=3 pt,\n"
            + "\ttitle/.style={%\n"
            + "\t\tnode font=\\Large,\n"
            + "\t},\n"
            + "\thournumber/.style={%\n"
            + "\t\tanchor=west,\n"
            + "\t\tnode font=\\small, \n"
            + "\t},\n"
            + "\tminutenumber/.style={%\n"
            + "\t\tanchor = west,\n"
            + "\t\tnode font=\\tiny, \n"
            + "\t\tcolor=gray,\n"
            + "\t},\n"
            + "\tyscale = -1]\n"
            + "\t% Framing Nodes\n"
            + "\t\\node at (0,0) {};\n"
            + "\t\\node at (11,17) {};\n"
            + "\t\n"
            + "\t% Date / Title and Border Lines\n"
            + "\t\\draw [thick] (0.5,1) -- (10.5,1);\n"
            + "\t\\draw [thick] (0.5, 16.5) -- (10.5, 16.5);\n"
            + "\t\\draw [thick] (0.5, 1) -- (0.5, 16.5);\n"
            + "\t\\draw [thick] (10.5, 1) -- (10.5, 16.5);\n"
            + "\n"
            + "\t% Hour Numbers\n"
            + "\t\\foreach \\i [evaluate=\\i as \\n using int(\\i+12)] in {0, 1, ..., 11}{\n"
            + "\t\t\\node [hournumber] at (0.5, \\i*15.5/12 + 1.3) {\\n};\n"
            + "\t}\n"
            + "\t\n"
            + "% Minute Numbers\n"
            + "\t\\foreach \\i in {0, 1, ..., 11}{\n"
            + "\t\t\\node [minutenumber] at (0.5, \\i*15.5/12 + 2) {:30};\n"
            + "\t}\n"
            + "\n"
            + "\t% Vertical Lines\n"
            + "\t\\draw (1,1) -- (1, 16.5);\n"
            + "\t\\foreach \\i in {1, 4.16673, ..., 10.5}{\n"
            + "\t\t\\draw (\\i, 1) -- (\\i, 16.5);\n"
            + "\t}\n"
            + "\n"
            + "\t% Minor Horizontal Lines\n"
            + "\t\\foreach \\i in {0.5, 1.5, ..., 11.5}{\n"
            + "\t\t\\draw [gray, thin] (1, \\i*15.5/12 + 1) -- (10.5, \\i*15.5/12 + 1);\n"
            + "\t}\n"
            + "\n"
            + "\t% Major Horizontal Lines\n"
            + "\t\\foreach \\i in {0, 1, ..., 11}{\n"
            + "\t\t\\draw (0.5, \\i*15.5/12 + 1) -- (10.5, \\i*15.5/12 + 1);\n"
            + "\t}\n"
            + "\t\n"
            + "\\end{tikzpicture}\n")

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

printYearly = input("Print yearly pages? (y/n): ") == "y"
printQuarterly = input("Print quarterly pages? (y/n): ") == "y"
printMonthly = input("Print monthly pages? (y/n): ") == "y"
printWeekly = input("Print weekly pages? (y/n): ") == "y"
printDaily = input("Print daily pages? (y/n): ") == "y"

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

############################################################

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

    if printYearly and y:
        printYear(output, startDate + timedelta(days=6))
    if printQuarterly and q:
        printQuarter(output, startDate + timedelta(days=6))
    if printMonthly and m:
        printMonth(output, startDate + timedelta(days=6))
    if printWeekly and w:
        printWeek(output, startDate)
    if printDaily and d:
        printDay(output, startDate)

    startDate += timedelta(days=1)

output.write("\\end{document}\n")

output.close()
