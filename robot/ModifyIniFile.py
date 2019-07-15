import re

# <----------------------------------------------------------------- Variables ----------------------------------------------------------------->
modify_file = "File Path"
modify_indicator = ''
modify_Id = ''
modify_Value = ''
modify_Replace = None

# <----------------------------------------------------------------- Functions ----------------------------------------------------------------->
def fetch_from_left(string, marker):
    return string.split(marker)[0]

def fetch_from_right(string, marker):
    return string.split(marker)[-1]

def strip_string(string, mode='both', characters=None):
    try:
        method = {'BOTH': string.strip,
                  'LEFT': string.lstrip,
                  'RIGHT': string.rstrip,
                  'NONE': lambda characters: string}[mode.upper()]
    except KeyError:
        raise ValueError("Invalid mode '%s'." % mode)
    return method(characters)

def replace(match):
    return replacements[match.group(0)]

# <------------------------------------------------------------------ Process ------------------------------------------------------------------>
#1. Open .ini file and read
file_ini = open(modify_file,"r",encoding="Shift_JIS")
text_ini = file_ini.read()

#2. Fetch the data under modify_indicator only
get_Start = fetch_from_right(text_ini, modify_indicator)
get_End = fetch_from_left(get_Start,'[')

#3. Remove leading and trailing whitespaces and newlines
strip_String = strip_string(get_End)

#4. Split lines to capture line value to be replaced with the new value
split_lines = str(strip_String)
for lines in split_lines.splitlines():
    get_id = lines.split('=')
    if(modify_Id == get_id[0]):
        modify_Replace = lines
        break

#5. Setting the replacement value = old value : new value        
replacements = {modify_Replace:modify_Id+'='+modify_Value}

#6. Apply modification on data under modify_indicator
modified_indicator = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, strip_String)

#7. Apply modified_indicator to the whole .ini file and overwrite the original .ini file
modified_ini = text_ini.replace(strip_String,modified_indicator)
pageSource = open(modify_file,"w+",1,encoding="Shift_JIS")
pageSource.write(modified_ini)