import re


class HttpHeader:
    def __init__(self, name, value, variables_in_value):
        self.name = name
        self.value = value
        self.variables_in_value = variables_in_value

    def __repr__(self):
        return "(" + self.name + ":" + self.value + ")"


class HttpTarget:

    def __init__(self, index):
        self.index = index
        self.name = None
        self.comment = None
        self.tags = []
        self.method = ""
        self.url = ""
        self.variables_in_url = False
        self.schema = None
        self.headers = []
        self.body = None
        self.variables_in_body = False
        self.body_lines = None
        self.script = None
        self.variables = []
        self.mock_result = None

    def is_empty(self):
        return self.method == "" and self.url == ""

    def is_mocked(self):
        return self.mock_result is not None

    def clean(self):
        if self.url != "":
            self.variables_in_url = "{{" in self.url
            self.url = self.replace_variables(self.url)
        if self.body is not None:
            self.variables_in_body = "{{" in self.body
            self.body = self.replace_variables(self.body)
        if self.name is None:
            self.name = "http" + self.index
        else:
            self.name = self.name.replace("-", "")
        mocked_lines = []
        for tag in self.tags:
            if tag.startswith("mock "):
                mocked_lines.append(tag[5:])
        if len(mocked_lines) > 0:
            self.mock_result = "\n".join(mocked_lines)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_header(self, name, value):
        variables_in_header = '{{' in value
        new_value = self.replace_variables(value)
        self.headers.append(HttpHeader(name, new_value, variables_in_header))

    def add_script_line(self, script_line):
        pass

    def add_body_line(self, body_line):
        if self.body is None:
            self.body = body_line
            self.body_lines = [body_line]
        else:
            self.body = self.body + "\n" + body_line
            self.body_lines.append(body_line)

    def replace_variables(self, text: str):
        new_text = text
        while "{{" in new_text:
            start = new_text.index("{{")
            end = new_text.index("}}")
            if end < start:
                return new_text
            name = new_text[start + 2:end]
            if name.startswith("$"):
                name = name[1:]
            if not (name in self.variables):
                self.variables.append(name)
            value = '{' + name + "}"
            new_text = new_text[0:start] + value + new_text[end + 2:]
        return new_text

    def extract_graphql_document(self):
        doc = {}
        variables_offset = -1
        variables_offset_end = -1
        for idx, l in enumerate(self.body_lines):
            line = l.strip()
            if line == "{":
                variables_offset = idx
            elif line == "}":
                variables_offset_end = idx
        if 0 < variables_offset < variables_offset_end:
            query = "\n".join(self.body_lines[0:variables_offset])
            doc['query'] = query
            doc['variables'] = "\n".join(self.body_lines[variables_offset:])
        else:
            doc['query'] = self.body
        return doc

    def to_api_declare(self):
        pass

    def to_mock_code(self):
        pass

    def to_function(self):
        pass


def parse_httpfile(httpfile_text: str):
    targets = []
    lines = httpfile_text.splitlines()
    index = 1
    http_target = HttpTarget(index)
    for l in lines:
        line = l.rstrip()
        if (line == "" or line.startswith("#!/usr/bin/env")) and http_target.is_empty():
            continue
        if line.startswith("###"):  # request seperator
            comment = line[3:].strip()
            if http_target.is_empty():
                http_target.comment = comment
            else:
                http_target.clean()
                targets.append(http_target)
                index = index + 1
                http_target = HttpTarget(index)
                http_target.comment = comment
        elif line.startswith("//") or line.startswith("#"):  # comment
            if "@" in line:
                tag = line[line.index('@') + 1:]
                parts = re.split("[=\\s]", tag, 2)
                if parts[0] == "name":
                    http_target.name = parts[1]
                http_target.add_tag(tag)
            elif http_target.comment == "":
                http_target.comment = line[2].strip()
        elif (line.startswith("GET ") or line.startswith("POST ")
              or line.startswith("DELETE") or line.startswith("PUT ")
              or line.startswith("GRAPHQL ")) and http_target.method == "":  # http method and URL
            parts = line.split(' ', 3)  # format as `POST URL HTTP/1.1`
            http_target.method = parts[0]
            http_target.url = parts[1].strip()
            if len(parts) > 2:
                http_target.schema = parts[2]
        elif line.startswith("  ") \
                and ('  /' in line or '  ?' in line or '  &' in line) \
                and len(http_target.headers) == 0:  # long request url into several lines
            http_target.url = http_target.url + line.strip()
        elif (":" in line) and (http_target.body is None) and (http_target.script is None):  # http header
            offset = line.index(':')
            http_target.add_header(line[0:offset].strip(), line[offset + 1:].strip())
        elif line.startswith("<> "):  # response-ref
            continue
        else:  # http body
            if not (line == "" and http_target.body is None):
                if line.startswith("> {%"):  # indicate script
                    code = line[4:].strip()
                    if code.endswith("5}"):
                        code = code[0:-2]
                    http_target.script = code
                elif line.startswith("%}"):  # end of script
                    continue
                elif line.startswith("> "):  # insert the script file
                    http_target.script = line
                else:
                    if http_target.script is not None:
                        http_target.add_script_line(l)
                    else:
                        http_target.add_body_line(l)

    if not http_target.is_empty():
        http_target.clean()
        targets.append(http_target)
    return targets
