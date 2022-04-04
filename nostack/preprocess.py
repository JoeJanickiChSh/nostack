

class PreProcessor:
    def __init__(self, code):
        self.code = code

    def remove_comments(self):
        out_code = ''
        scan = True
        for c in self.code:
            if c == '\\':
                scan = not scan
            elif scan:
                out_code += c
        self.code = out_code

    def replace_char(self):
        out_code = ''
        scan = False
        for c in self.code:
            if c == "'":
                scan = not scan
            elif scan:
                out_code += str(ord(c))
            else:
                out_code += c

        self.code = out_code

    def replace_string(self):
        out_code = ''
        scan = False
        for c in self.code:
            if c == '"':
                scan = not scan
                if scan:
                    out_code += '['
                else:
                    out_code += '0]'
            elif scan:
                out_code += str(ord(c)) + ', '
            else:
                out_code += c

        self.code = out_code

    def import_code(self):
        lines = self.code.split('\n')
        out_lines = []
        for line in lines:
            split = line.split()
            if len(split) > 0:
                if split[0] == '.import':
                    with open(split[1] + '.mcl', 'r') as fp:
                        in_code = fp.read()
                    out_lines.append(in_code)
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)

        self.code = '\n'.join(out_lines)

    def process(self):
        for i in range(64):
            self.import_code()
        self.remove_comments()
        self.replace_char()
        self.replace_string()
        return self.code.replace(' ', '').replace('\n', '').replace('\t', '')
