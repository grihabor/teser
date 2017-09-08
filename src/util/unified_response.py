
class UnifiedResponse:
    def __init__(self, *, result, details):
        self.result = result
        self.details = details

    def __iter__(self):
        yield 'result', self.result
        yield 'details', self.details

