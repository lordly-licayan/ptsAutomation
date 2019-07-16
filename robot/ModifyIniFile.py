import re
import json

def modify_ini_file(file, x_dictionary, x_encoding):
    # Convert Dictionary to Json
    dictionary = json.dumps(x_dictionary)
    newJson = json.loads(dictionary)

    # <----------------------------------------------------------------- Variables ----------------------------------------------------------------->
    modify_file = file
    modify_Value = None
    modify_isSuccess = None

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

    def enclose(str, word):
        return str[:1] + word + str[1:]

    # <------------------------------------------------------------------ Process ------------------------------------------------------------------>
    # Open .ini file and read
    file_ini = open(modify_file,"r",encoding=x_encoding)
    text_ini = file_ini.read()
    original_ini = text_ini

    # Check if section exists
    for modify_section in newJson:
        if(str(text_ini).find(modify_section) == -1):
            modify_isSuccess = "Error: " + modify_section + " section does not exist in file."
            return modify_isSuccess

    # Fetch the data under modify_section only
    for modify_section in newJson:
        get_Start = fetch_from_right(text_ini, modify_section)
        get_End = fetch_from_left(get_Start,'[')

        # Remove leading and trailing whitespaces and newlines
        strip_String = strip_string(get_End)
        original_stripped = strip_String

        for info in newJson.get(modify_section):
            new_id = info
            new_value = newJson.get(modify_section)[info]
            get_enclosed = None
            key_exists = False

            # Split lines to capture line value to be replaced with the new value
            split_lines = str(strip_String)
            for lines in split_lines.splitlines():
                get_id = lines.split('=')
                if(str(info).lower() == str(get_id[0]).lower()):
                    modify_Value = lines
                    key_exists = True
                    try:
                        get_id[1] = get_id[1].replace(" ", "")
                        get_enclosed = get_id[1][0]
                        if("\"" == get_enclosed):
                            new_value = enclose("\"\"", new_value)
                        elif("'" == get_enclosed):
                            new_value = enclose("''", new_value)
                    except:
                        pass
                    break

            # Check if key exists
            if(not key_exists):
                modify_isSuccess = "Error: " + info + " key does not exist in " + modify_section + " section."
                return modify_isSuccess

            # Setting the replacement value = old value : new value
            replacements = {modify_Value:new_id+'='+new_value}
            x_pattern = '|'.join(r'\b%s\b' % re.escape(s) for s in replacements)

            # Apply modification on data under modify_section
            modified_section = re.sub(x_pattern, replace, strip_String)
            if(modified_section == split_lines):
                modified_section = modified_section.replace(modify_Value, new_id+'='+new_value)
            strip_String = modified_section

        # Apply modified_section to the .ini file
        modified_ini = text_ini.replace(original_stripped,strip_String)
        text_ini = modified_ini

    if(original_ini != text_ini):
        pageSource = open(modify_file,"w+",1,encoding=x_encoding)
        pageSource.write(modified_ini)
        modify_isSuccess = True
    else:
        modify_isSuccess = 'File not modified.'

    return modify_isSuccess