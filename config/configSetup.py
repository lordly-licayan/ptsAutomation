import xml.etree.ElementTree as ET 

tagRegEx= ".//pteInfo/*"

def parseXML(xmlfile, findTags = tagRegEx): 
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    tagNames = {t.tag for t in root.findall(findTags)}
    resultList= {}

    for tag in tagNames:
        for child in root:
            resultList[tag] = child.find(tag).text

    return resultList