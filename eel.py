import sys
import textwrap

def debug(*args):
    pass
    # print '[dbg]', ' '.join(str(a) for a in args)

class Interpreter:
    acc = 0
    acc2 = 0
    defined = {}
    commands = []

    def compile(self, program):
        program = textwrap.dedent(program).strip()
        lines = program.split("\n")
        lines.reverse()
        self.commands += lines

        while self.commands:
            command = self.commands.pop()
            debug('==> running:', command, 'stack:', self.commands)
            self.run_command(command)

    def run_command(self, cmd):
        if cmd.startswith("def(") and cmd.endswith(")"):
            name, code = cmd[4:-1].split('|')
            self.defined[name] = code.split(';')
            debug('::found def', self.defined)

        elif cmd in self.defined:
            debug('::found defined name', cmd, '=>', str(self.defined[cmd]))
            self.commands += ['$marker']  
            self.commands += list(reversed(self.defined[cmd]))

        elif cmd == '$marker':
            pass

        elif cmd == 'x':
            if self.acc == 0:
                while self.commands:
                    tmp = self.commands.pop()
                    if tmp == '$marker':
                        break

        elif cmd == "i":
            self.acc = int(input(">> "))

        elif cmd == "p":
            print(self.acc)

        elif cmd == "c":
            print(chr(self.acc))

        elif cmd == "s":
            t = self.acc
            t2 = self.acc2
            self.acc = t2
            self.acc2 = t

        elif cmd == "a":
            self.acc += self.acc2

        elif cmd == "S":
            self.acc -= self.acc2

        else:
            self.acc += int(cmd)

intp = Interpreter()

try:
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    intp.compile(str(code))

except IndexError:
    while 1:
        intp.compile(input("> "))
