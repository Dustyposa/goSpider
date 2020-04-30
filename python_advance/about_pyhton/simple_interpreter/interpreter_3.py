# https://qingyunha.github.io/taotao/

import collections
import dis
import inspect
import sys
import types


class VirtualMachineError(Exception):
    pass


Block = collections.namedtuple("Block", "type, handler, stack_height")


class VirtualMachine(object):
    def __init__(self):
        self.frames = []  # The call stack of frames.
        self.frame = None  # The current frame.
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names=None, local_names=None):
        """ An entry point to execute code using the virtual machine."""
        frame = self.make_frame(
            code,
            global_names=global_names,
            local_names=local_names
        )
        self.run_frame(frame)

    def make_frame(self, code, callargs=None, global_names=None, local_names=None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None,
            }
        if isinstance(callargs, dict):
            local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return Frame

    def push_frame(self, frame) -> None:
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self) -> None:
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None

    def run_frame(self, frame):
        """Run a frame until it returns (somehow).
        Exceptions are raised, the return value is returned.
        """
        self.push_frame(frame)
        while True:
            byte_name, arguments = self.parse_byte_and_args()

            why = self.dispatch(byte_name, arguments)

            # Deal with any block management we need to do
            while why and frame.block_stack:
                why = self.manage_block_stack(why)

            if why:
                break

        self.pop_frame()

        if why == 'exception':
            exc, val, tb = self.last_exception
            e = exc(val)
            e.__traceback__ = tb
            raise e

        return self.return_value

    # 数据栈操作
    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        self.frame.stack.pop()

    def push(self, *vals):
        self.frame.stack.extend(vals)

    def popn(self, n):
        """Pop a number of values from the value stack.
        A list of `n` values is returned, the deepest value first.
        """
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []

    def parse_byte_and_args(self):
        f = self.frame
        opoffset = f.last_instruction
        byte_code = f.code_obj.co_code[opoffset]
        f.last_instruction += 1
        byte_name = dis.opname[byte_code]
        if byte_code >= dis.HAVE_ARGUMENT:
            # index into the bytecode
            arg = f.code_obj.co_code[f.last_instruction:f.last_instruction + 2]
            f.last_instruction += 2  # advance the instruction pointer
            arg_val = arg[0] + (arg[1] * 256)
            if byte_code in dis.hasconst:  # Look up a constant
                arg = f.code_obj.co_consts[arg_val]
            elif byte_code in dis.hasname:  # Look up a name
                arg = f.code_obj.co_names[arg_val]
            elif byte_code in dis.haslocal:  # Look up a local name
                arg = f.code_obj.co_varnames[arg_val]
            elif byte_code in dis.hasjrel:  # Calculate a relative jump
                arg = f.last_instruction + arg_val
            else:
                arg = arg_val
            argument = [arg]
        else:
            argument = []

        return byte_name, argument

    def dispatch(self, byte_name, argument):
        """ Dispatch by bytename to the corresponding methods.
        Exceptions are caught and set on the virtual machine."""

        # When later unwinding the block stack,
        # we need to keep track of why we are doing it.
        why = None
        try:
            bytecode_fn = getattr(self, 'byte_%s' % byte_name, None)
            if bytecode_fn is None:
                if byte_name.startswith('UNARY_'):
                    self.unaryOperator(byte_name[6:])
                elif byte_name.startswith('BINARY_'):
                    self.binaryOperator(byte_name[7:])
                else:
                    raise VirtualMachineError(
                        "unsupported bytecode type: %s" % byte_name
                    )
            else:
                why = bytecode_fn(*argument)
        except:
            # deal with exceptions encountered while executing the op.
            self.last_exception = sys.exc_info()[:2] + (None,)
            why = 'exception'

        return why

        # Block stack manipulation
        def push_block(self, b_type, handler=None):
            level = len(self.frame.stack)
            self.frame.block_stack.append(Block(b_type, handler, stack_height))

        def pop_block(self):
            return self.frame.block_stack.pop()

        def unwind_block(self, block):
            """Unwind the values on the data stack corresponding to a given block."""
            if block.type == 'except-handler':
                # The exception itself is on the stack as type, value, and traceback.
                offset = 3
            else:
                offset = 0

            while len(self.frame.stack) > block.level + offset:
                self.pop()

            if block.type == 'except-handler':
                traceback, value, exctype = self.popn(3)
                self.last_exception = exctype, value, traceback

        def manage_block_stack(self, why):
            """ """
            frame = self.frame
            block = frame.block_stack[-1]
            if block.type == 'loop' and why == 'continue':
                self.jump(self.return_value)
                why = None
                return why

            self.pop_block()
            self.unwind_block(block)

            if block.type == 'loop' and why == 'break':
                why = None
                self.jump(block.handler)
                return why

            if block.type in ['setup-except', 'finally'] and why == 'exception':
                self.push_block('except-handler')
                exctype, value, tb = self.last_exception
                self.push(tb, value, exctype)
                self.push(tb, value, exctype)  # yes, twice
                why = None
                self.jump(block.handler)
                return why

            elif block.type == 'finally':
                if why in ('return', 'continue'):
                    self.push(self.return_value)

                self.push(why)

                why = None
                self.jump(block.handler)
                return why
            return why


class Frame(object):
    def __init__(self, code_obj, global_names, local_names, prev_frame):
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        self.block_stack = []


class Function(object):
    """
    Create a realistic function object, defining the things the interpreter expects.
    """
    __slots__ = [
        'func_code', 'func_name', 'func_defaults', 'func_globals',
        'func_locals', 'func_dict', 'func_closure',
        '__name__', '__dict__', '__doc__',
        '_vm', '_func',
    ]

    def __init__(self, name, code, globs, defaults, closure, vm):
        """You don't need to follow this closely to understand the interpreter."""
        self._vm = vm
        self.func_code = code
        self.func_name = self.__name__ = name or code.co_name
        self.func_defaults = tuple(defaults)
        self.func_globals = globs
        self.func_locals = self._vm.frame.f_locals
        self.__dict__ = {}
        self.func_closure = closure
        self.__doc__ = code.co_consts[0] if code.co_consts else None

        # Sometimes, we need a real Python function.  This is for that.
        kw = {
            'argdefs': self.func_defaults,
        }
        if closure:
            kw['closure'] = tuple(make_cell(0) for _ in closure)
        self._func = types.FunctionType(code, globs, **kw)

    def __call__(self, *args, **kwargs):
        """When calling a Function, make a new frame and run it."""
        callargs = inspect.getcallargs(self._func, *args, **kwargs)
        # Use callargs to provide a mapping of arguments: values to pass into the new
        # frame.
        frame = self._vm.make_frame(
            self.func_code, callargs, self.func_globals, {}
        )
        return self._vm.run_frame(frame)


def make_cell(value):
    """Create a real Python closure and grab a cell."""
    # Thanks to Alex Gaynor for help with this bit of twistiness.
    fn = (lambda x: lambda: x)(value)
    return fn.__closure__[0]
