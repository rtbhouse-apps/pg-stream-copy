class MockPsycopg2CopyExpert:
    query: str
    data: bytes

    def __init__(self):
        self.query = None
        self.data = None

    def copy_expert(self, query, stream):
        assert not self.query
        assert not self.data

        self.query = query
        self.data = stream.read()
