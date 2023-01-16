
import xml.etree.ElementTree as et
import pandas as pd
import requests
import os

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

URL = 'https://www.bsi.si/_data/tecajnice/dtecbs-l.xml'
response = requests.get(URL)

with open('feed.xml', 'wb') as file:
    file.write(response.content)

tree = et.parse(f"{dir}\\feed.xml")
root = tree.getroot()

curr_symb = []
for x in root[len(root)-1]:
    curr_symb.append(str(x.attrib))

curr_symb = [i[12:15] for i in curr_symb]
print(curr_symb)

xml_data = open(dir + '\\feed.xml', 'r').read()  # Read file

root = et.XML(xml_data)  # Parse XML

data = []
cols = []
for i, child in enumerate(root):
    data.append([subchild.text for subchild in child])
    cols.append(child.attrib)

cols = [str(i) for i in cols]
cols = [i.replace("{'datum': '","") for i in cols]
cols = [i.replace("'}","") for i in cols]

df = pd.DataFrame(data).T  # Write in DF and transpose it
df.columns = cols  # Update column names

df = df.stack().str.replace('.',',').unstack()

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer)
writer.save()
print('Data successfully exported to Excel File.')