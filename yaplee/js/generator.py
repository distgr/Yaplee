class Generator:
    def __init__(self) -> None:
        pass
    
    def format_entry(self, entry, getstr=False):
        if type(entry) == str:
            to_return = self.fstr(entry)

        elif type(entry) == list:
            to_return = self.farray(entry)

        if type(entry) == int:
            to_return = '{}'.format(entry)

        return (str(to_return) if getstr else to_return)

    def fstr(self, string) -> str:
        return '"{}"'.format(string.replace('"', '\\"'))
    
    def farray(self, _list):
        return '[{}]'.format(
            ', '.join([self.format_entry(i, getstr=True) for i in _list])
        )
    
    def call(self, callable, params) -> str:
        param_list = list(self.format_entry(i) for i in params)
        
        return "{}({});".format(
            str(callable),
            ', '.join(param_list)
        )