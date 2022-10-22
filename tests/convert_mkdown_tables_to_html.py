# coding: utf-8
from rich import print
import re


with open('../README.md') as f:
    readme = f.read()

regex = r'(?<=\|)\s*(.+?)\s*(?=\|)'
r = re.compile(regex)
in_table = False
for line in readme.splitlines():
    if re.search(r'# \d+\.', line):
        print(f'{"-"*80}\n{line}\n{"-"*80}')
    if r.search(line):
        items = r.findall(line)
        if in_table == False:
            in_table = True
            table = '<table>\n'
            headers = '<tr>'
        #table += '<tr>\n'
        row = '<tr>'
        for i, item in enumerate(items):
            if item[0].isupper() and item[-1].islower():
                headers += f'<td> {item} </td>'
            elif ':--' in item or '--:' in item:
                if i == 0:
                    headers += '</tr>\n'
            else:
                item = item.replace('**', '').replace('`', '')
                if '?' in item:
                    # is params
                    row += f'\n<td>\n\n```erlang\n{item}\n```\n\n</td>'
                elif item.strip().startswith('/'):
                    # is url_path
                    row += f'\n<td>\n\n```jq\n{item}\n```\n\n</td>'
                else:
                    # is statement
                    row += f'\n<td>\n\n```rexx\n{item}\n```\n\n</td>'
        row += '\n</tr>\n'
        if len(row) > 11:
            table += headers + row
        #break
    else:
        if in_table == True:
            in_table = False
            table += '</table>\n'
            print(table)
""
