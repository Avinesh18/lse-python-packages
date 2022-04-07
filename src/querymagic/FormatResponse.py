import pandas

def formatResponse(result, format):
    if format == "df":
        return pandas.DataFrame(result['rows'], columns = result['columns'])
    elif format == "raw":
        return result
    elif format == "table":
        return generateTable()
    else:
        return pandas.DataFrame(result['rows'], columns = result['columns'])

def generateTable():
    # TODO
    pass