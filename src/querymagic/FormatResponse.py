import re
from textwrap import wrap
import pandas
import numpy as np
from IPython.display import display
from dateutil.parser import parse
import matplotlib.pyplot as plt
from pandas.plotting import table
from .Chart import plotChart
from .Table import generateTable

def formatResponse(result, options):
    fig = None

    if not('out' in options):
        display(pandas.DataFrame(result['rows'], columns = result['columns']))

    elif options['out'] == 'table':
        fig = generateTable(result, options)

    elif options['out'] == "raw":
        display(result)

    elif options['out'] == 'chart':
        fig = plotChart(result, options)

    else:
        fig = generateTable(result, options)

    return fig
