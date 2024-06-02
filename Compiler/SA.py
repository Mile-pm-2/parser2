import re


class Parser:
    def __init__(self, input_str):
        self.tokens = re.findall(r'\w+|[{}(),;:=<>+\-*/]', input_str)
        self.pos = 0

    def expect(self, expected_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == expected_token:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected '{expected_token}', got '{self.tokens[self.pos]}' at position {self.pos}")

    def P(self):
        self.expect('{')
        self.D1()
        self.S1()
        self.expect('}')

    def D1(self):
        if self.pos < len(self.tokens) and re.match(r'[a-z]', self.tokens[self.pos]):
            self.D()
            while self.pos < len(self.tokens) and self.tokens[self.pos] == ',':
                self.expect(',')
                self.D()
            self.expect(';')

    def D(self):
        self.I1()
        self.expect(':')
        self.type()

    def type(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos] in ['int', 'real', 'boolean']:
            self.pos += 1
        else:
            raise SyntaxError(
                f"Expected type (int, real, boolean), got '{self.tokens[self.pos]}' at position {self.pos}")

    def I1(self):
        self.I()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == ',':
            self.expect(',')
            self.I()

    def S1(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos] != '}':
            self.S()
            while self.pos < len(self.tokens) and self.tokens[self.pos] == ';':
                self.expect(';')
                self.S()
        # Убедимся, что парсер завершает работу, если достигнут конец программы
        if self.pos < len(self.tokens) and self.tokens[self.pos] == '}':
            self.expect('}')

    def S(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == 'if':
            self.expect('if')
            self.E()
            self.expect('then')
            self.S()
            self.expect('else')
            self.S()
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == 'while':
            self.expect('while')
            self.E()
            self.expect('do')
            self.S()
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == 'for':
            self.expect('for')
            self.I()
            self.expect('ass')
            self.E()
            self.expect('to')
            self.E()
            self.expect('do')
            self.S1()
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == 'read':
            self.expect('read')
            self.expect('(')
            self.I()
            self.expect(')')
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == 'writeln':
            self.expect('writeln')
            self.expect('(')
            if self.pos < len(self.tokens) and re.match(r'[a-z]', self.tokens[self.pos]):
                self.I1()
            else:
                self.E()
            self.expect(')')
        else:
            self.I()
            self.expect('ass')
            self.E()

    def E(self):
        self.E1()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ['=', '>', '<', '<>', '<=', '>=']:
            self.pos += 1
            self.E1()

    def E1(self):
        self.T()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ['+', '-', 'or']:
            self.pos += 1
            self.T()

    def T(self):
        self.F()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ['*', '/', 'and']:
            self.pos += 1
            self.F()

    def F(self):
        if self.pos < len(self.tokens) and re.match(r'[a-z]', self.tokens[self.pos]):
            self.I()
        elif self.pos < len(self.tokens) and self.tokens[self.pos].isdigit():
            self.N()
        elif self.pos < len(self.tokens) and self.tokens[self.pos] in ['true', 'false']:
            self.pos += 1
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == 'not':
            self.expect('not')
            self.F()
        elif self.pos < len(self.tokens) and self.tokens[self.pos] == '(':
            self.expect('(')
            self.E()
            self.expect(')')
        else:
            raise SyntaxError(f"Unexpected token '{self.tokens[self.pos]}' at position {self.pos}")

    def I(self):
        if self.pos < len(self.tokens) and re.match(r'[a-z]', self.tokens[self.pos]):
            self.pos += 1
        else:
            raise SyntaxError(f"Expected identifier, got '{self.tokens[self.pos]}' at position {self.pos}")

    def N(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos].isdigit():
            self.pos += 1
            while self.pos < len(self.tokens) and self.tokens[self.pos].isdigit():
                self.pos += 1
        else:
            raise SyntaxError(f"Expected number, got '{self.tokens[self.pos]}' at position {self.pos}")


# Test the parser with the corrected example
test_input = '''
{a,b,del: int;
read(a); 
read(b); 
del ass a/b;
writeln(del);}
'''
parser = Parser(test_input)
try:
    parser.P()
    print("Parsing successful!")
except SyntaxError as e:
    print(f"Syntax error: {e}")
