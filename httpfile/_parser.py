class HttpTarget:
    index = 0
    name = None
    comment = ""
    tags = []
    method = ""
    url = ""
    headers = []
    body = None
    body_lines = []
    script = None
    variables = []
    mock_result = None

    def __int__(self, index):
        self.index = index

    def is_empty(self):
        return self.method != "" and self.url != ""

    def is_mocked(self):
        return self.mock_result is not None

    def clean(self):
        pass

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_header(self, name, value):
        self.headers.append((name, value))

    def add_script_line(self, script_line):
        pass

    def add_body_line(self, body_line):
        self.body_lines.append(body_line)

    def replace_variables(self, text):
        pass

    def extract_graphql_document(self):
        pass

    def to_api_declare(self):
        pass

    def to_mock_code(self):
        pass

    def to_function(self):
        pass


def parse_httpfile(httpfile_text):
    pass
