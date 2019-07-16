import re
import json

def modify_ini_file(file, x_dictionary, x_encoding):
    # Convert Dictionary to Json
    dictionary = json.dumps(x_dictionary)
    newJson = json.loads(dictionary)

    # <----------------------------------------------------------------- Variables ----------------------------------------------------------------->
    modify_file = file
    modify_Replace = None
    modify_isSuccess = False

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

    # Fetch the data under modify_category only
    for modify_category in newJson:
        get_Start = fetch_from_right(text_ini, modify_category)
        get_End = fetch_from_left(get_Start,'[')

        # Remove leading and trailing whitespaces and newlines
        strip_String = strip_string(get_End)
        original_stripped = strip_String

        for info in newJson.get(modify_category):
            for modify_Id in info:
                modify_Value = info[modify_Id]
                get_enclosed = None

                # Split lines to capture line value to be replaced with the new value
                split_lines = str(strip_String)
                for lines in split_lines.splitlines():
                    get_id = lines.split('=')
                    if(modify_Id == get_id[0]):
                        modify_Replace = lines
                        try:
                            get_enclosed = get_id[1][0]
                            if("\"" in get_enclosed):
                                modify_Value = enclose("\"\"", modify_Value)
                            elif("'" in get_enclosed):
                                modify_Value = enclose("''", modify_Value)
                        except:
                            pass
                        break

                # Setting the replacement value = old value : new value
                replacements = {modify_Replace:modify_Id+'='+modify_Value}

                # Apply modification on data under modify_category
                modified_category = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, strip_String)
                if(modified_category == split_lines):
                    modified_category = modified_category.replace(modify_Replace, modify_Id+'='+modify_Value)
                strip_String = modified_category

        # Apply modified_category to the .ini file
        modified_ini = text_ini.replace(original_stripped,strip_String)
        text_ini = modified_ini

    if(original_ini != text_ini):
        pageSource = open(modify_file,"w+",1,encoding=x_encoding)
        pageSource.write(modified_ini)
        modify_isSuccess = True
    else:
        print('Not modified')

    return modify_isSuccess