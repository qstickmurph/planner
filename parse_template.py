import re
from datetime import date, timedelta

def evaluate(match_obj):
    return str(eval(match_obj.group(1)))

def parse_template(templateFolder, fileName, **kwargs):
    globals().update(kwargs)
    if not fileName.endswith('.template'):
        fileName += '.template'
    with open(templateFolder+'/'+fileName, 'r') as template:
        read = template.read()
        regexString = r'{{([^{]*?)}}'
        return re.sub(regexString, evaluate, read)

#print(parse_template("templates/quarter-with-daily-notes", "day", test="test"))