import matplotlib.pyplot as plt
import pandas
from pandas.plotting import table

MAX_CHARACTERS_IN_ONE_LINE = 30
count = 1

def break_text_into_lines(text):
    return '\n'.join(text[i:i+MAX_CHARACTERS_IN_ONE_LINE] for i in range(0, len(text), MAX_CHARACTERS_IN_ONE_LINE))

def getTexTable(rows, columns, title = ""):
    tex_begin = """\\documentclass[landscape]{article}
\\usepackage{graphicx}
\\usepackage[left=0in,
            right=0in,
            top=0.2in,
            bottom=0.2in]{geometry}
\\usepackage{tabulary}
\\begin{document}\n"""

    tex_end = "\\end{document}"
    
    tex_table = tex_begin
    indentation = 'L'*len(columns)
    tex_table += """\\begin{table}[ht]
\\begin{tabulary}{0.95\\textwidth}{"""
    
    tex_table += indentation + "}\n\\hline\n"
    for i in range(len(columns) - 1):
        tex_table += str(columns[i]).replace("{", "\\{").replace("}", "\\}").replace(":", ": ").replace(",", ", ").replace("_", "\_").replace("#", "\#").replace("&", "\&") + " & "
    tex_table += str(columns[len(columns) - 1]).replace("{", "\\{").replace("}", "\\}").replace(":", ": ").replace(",", ", ").replace("_", "\_").replace("#", "\#").replace("&", "\&") + " \\\\\n\\hline\\hline\n"
    
    for row in rows:
        for i in range(len(row) - 1):
            tex_table += str(row[i]).replace("{", "\\{").replace("}", "\\}").replace(":", ": ").replace(",", ", ").replace("_", "\_").replace("#", "\#").replace("&", "\&") + " & "
        tex_table += str(row[len(row) - 1]).replace("{", "\\{").replace("}", "\\}").replace(":", ": ").replace(",", ", ").replace("_", "\_").replace("#", "\#").replace("&", "\&") + " \\\\\\hline\n"
    tex_table += "\\hline\n\\end{tabulary}\n"
    tex_table += "\\caption{" + title.replace("{", "\{").replace("}", "\}").replace(":", ": ").replace(",", ", ").replace("_", "\_").replace("#", "\#").replace("&", "\&") + "}\n\\end{table}\n"
    tex_table += tex_end
    
    return tex_table

def generateTable(result, options):
    global count
    title = options['title'] if 'title' in options else 'table' + str(count)
    tex_source = getTexTable(result['rows'], result['columns'], title)

    filename = "table" + str(count) + ".tex"
    count += 1
    try:
        f = open(filename, "w")
        f.write(tex_source)
    finally:
        f.close()