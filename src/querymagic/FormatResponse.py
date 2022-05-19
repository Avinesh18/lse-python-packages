import pandas
from IPython.display import display
from .Table import generateTable
from .Chart import plotChart

def formatResponse(result, options):
    if not('out' in options):
        display(pandas.DataFrame(result['rows'], columns = result['columns']))

    elif options['out'] == 'table':
        generateTable(result, options)

    elif options['out'] == "raw":
        display(result)

    elif options['out'] == 'chart':
        plotChart(result, options)

    else:
        generateTable(result, options)