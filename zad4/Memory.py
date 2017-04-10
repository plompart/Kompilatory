class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.dictionary = {}

    def has_key(self, name):  # variable name
        return name in self.dictionary

    def get(self, name):  # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.dictionary[name]
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.dictionary[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = []
        if memory is not None:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("root"))

    def get(self, name):  # gets from memory stack current value of variable <name>
        i = len(self.stack) - 1
        while i >= 0:
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
            i -= 1
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.get_last_memory().put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        i = len(self.stack) - 1
        while i >= 0:
            if self.stack[i].has_key(name):
                self.stack[i].put(name, value)
                break
            i -= 1

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop()

    def get_global_value(self, funcName, name):
        memory = self.get_memory(funcName)
        index = self.return_index(memory)
        while index >= 0:
            if self.stack[index].has_key(name):
                return self.stack[index].get(name)
            index -= 1
        return None

    def set_global_value(self, funcName, name, value):
        memory = self.get_memory(funcName)
        index = self.return_index(memory)
        while index >= 0:
            if self.stack[index].has_key(name):
                self.stack[index].put(name, value)
                break
            index -= 1

    def get_last_memory(self):
        if len(self.stack) != 0:
            return self.stack[len(self.stack) - 1]
        else:
            return None

    def get_memory(self, name):  # get memory that contains variable name
        i = len(self.stack) - 1
        while i >= 0:
            if self.stack[i].has_key(name):
                return self.stack[i]
            i -= 1
        return self.stack[0]

    def return_index(self, memory):
        indices = range(len(self.stack))
        for i in range(len(self.stack)):
            if memory == self.stack[i]:
                return i


class FunctionStack(MemoryStack):
    def __init__(self):
        self.stack = []

    def set(self, name, value):
        if self.stack[-1].has_key(name):
            self.stack[-1].put(name, value)

    def get(self, name):
        if len(self.stack) != 0:
            if self.stack[-1].has_key(name):
                return self.stack[-1].get(name)
        return None
