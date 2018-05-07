#! /usr/bin/python
import sys
import array
import argparse
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

#root of xmltree
people = ET.Element('people');

def buildSubTree(personInfo, parent, id):
    for i, item in enumerate(personInfo):
        elem = item[0].split('|');
        elem.append(item[1]);
        if elem[0] == 'P':
            if elem[1] is not '':
                firstName = ET.SubElement(parent, 'First name');
                firstName.text = elem[1];
            if elem[2] is not '':
                lastName = ET.SubElement(parent, 'Last name');
                lastName.text = elem[2];

        elif elem[0] == 'F' and id is 'f':
            if elem[1] is not '':
                name = ET.SubElement(parent, 'Name');
                name.text = elem[1];
            if elem[2] is not '':
                born = ET.SubElement(parent, 'Born');
                born.text = elem[2];

        elif elem[0] == 'F' and id is not 'f':
            familyList = personInfo[i:len(personInfo)];
            makeXmlTree(familyList, 'F', parent);
            break;

        elif elem[0] == 'T':
            phone = ET.SubElement(parent, 'Phone');
            if elem[1] is not '':
                mobile = ET.SubElement(phone, 'Mobile');
                mobile.text = elem[1];
            if elem[2] is not '':
                landline = ET.SubElement(phone, 'Landline');
                landline.text = elem[2];

        elif elem[0] == 'A':
            address = ET.SubElement(parent, 'Address');
            if elem[1] is not '':
                street = ET.SubElement(address, 'Street');
                street.text = elem[1];
            if elem[2] is not '':
                city = ET.SubElement(address, 'City');
                city.text = elem[2];
            if elem[3] is not '':
                zipCode = ET.SubElement(address, 'Zip');
                elem[3].rstrip();
                zipCode.text = elem[3];


#--------------------------------------------------------------------#

def prettify(elem, level=0):
    i = "\n" + level*'  ';
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  ';
        if not elem.tail or not elem.tail.strip():
            elem.tail = i;
        for elem in elem:
            prettify(elem, level+1);
        if not elem.tail or not elem.tail.strip():
            elem.tail = i;
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i;


#--------------------------------------------------------------------#

def makeXmlTree(set, stop, parent):
    personInfo = [];
    for i, line in enumerate(set):
        if stop is 'P':
            ctrlChar = line[0];
            personInfo.append(line.split('\n'));
        elif stop is 'F':
            ctrlChar = line[0][0];
            personInfo.append(line);
        if i is not 0 and ctrlChar is stop:
            lastIndex = personInfo.pop();
            if stop is 'P':
                buildSubTree(personInfo, ET.SubElement(parent, 'Person'), 'p');
            elif stop is 'F':
                buildSubTree(personInfo, ET.SubElement(parent, 'Family'), 'f');
            personInfo = [];
            personInfo.append(lastIndex);
            i += 1;
    if personInfo:
        if stop is 'P':
            buildSubTree(personInfo, ET.SubElement(parent, 'Person'), 'p');
        elif stop is 'F':
            buildSubTree(personInfo, ET.SubElement(parent, 'Family'), 'f');


#--------------------------------------------------------------------#

def main():
    fileName = sys.argv[1:][0];
    outputFileName = 'data.xml';
    if len(sys.argv) is 3:
        outputFileName = sys.argv[1:][1];

    with open(fileName) as file:
        makeXmlTree(file, 'P', people);


    prettify(people);
    tree = ET.ElementTree(people);
    tree.write(outputFileName, xml_declaration=True, encoding='utf-8', method="xml");


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert textinfo to XML format')
    parser.add_argument('input', metavar='Files', type=str, nargs='+',
    help='<InputFile> | <InputFile> <OutputFile> | Outputfile is optional, default is data.xml')

    args = parser.parse_args()
    main();
