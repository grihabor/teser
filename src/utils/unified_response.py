
class UnifiedResponse(dict):
    def __init__(self, *, result, details):
        super().__init__()
        self['result'] = result
        self['details'] = details

    @property
    def result(self):
        return self['result']

    @property
    def details(self):
        return self['details']
