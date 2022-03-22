from IPython.core.magic import Magics, magics_class, cell_magic, needs_local_scope
from IPython.display import display
from .FetchResult import fetch_kusto, fetch_splunk
from .FormatResponse import formatSplunkResponse
from .Util import add_substitutions
import threading
import pandas
import re as regex

threadLock = threading.Lock()
SPLUNK_VALID_OUTPUT_MODES = ["df", "json", "table"]

class QueryResult(Magics):
    def __init__(self, type=None, query=None, result=None):
        self.__type = type
        self.__query = query
        self.__result = result

    @property
    def type(self):
        return self.__type

    @property
    def query(self):
        return self.__query
    
    @property
    def result(self):
        return self.__result

    def set(self, type, query, result):
        self.__type = type
        self.__query = query
        self.__result = result

_last_query_result = QueryResult()

@magics_class
class QueryMagic(Magics):

    def __init__(self, shell):
        super(QueryMagic, self).__init__(shell)

    @needs_local_scope
    @cell_magic
    def splunk(self, line, cell, local_ns=None):
        output_mode = "df"
        options = regex.findall("-(\w+)[ ]+(\w*)", line)
        for option in options:
            if option[0] == 'out':
                if option[1] in SPLUNK_VALID_OUTPUT_MODES:
                    output_mode = option[1]
        
        substituted_string = add_substitutions(cell, local_ns)
        try:
            threadLock.acquire()
            result = fetch_splunk(substituted_string)

            global _last_query_result
            _last_query_result.set("splunk", substituted_string, result)
            display(formatSplunkResponse(result, output_mode))
        finally:
            threadLock.release()

ip = get_ipython()
ip.register_magics(QueryMagic)