from .Util import valid_filename

count = 1

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
    title = None
    if 'title' in options:
        title = options['title']
    else:
        title = 'table' + str(count)
        count += 1

    tex_source = getTexTable(result['rows'], result['columns'], title)

    if valid_filename(title):
        filename = title + '.tex'
    else:
        filename = 'table' + str(count) + '.tex'
        count += 1
    try:
        f = open(filename, "w")
        f.write(tex_source)
    finally:
        f.close()