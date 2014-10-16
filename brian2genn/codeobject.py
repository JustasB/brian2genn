from brian2.devices.cpp_standalone.codeobject import CPPStandaloneCodeObject
from brian2.codegen.generators.cpp_generator import c_data_type, CPPCodeGenerator
from brian2.codegen.targets import codegen_targets
from brian2.codegen.templates import Templater

__all__ = ['GeNNCodeObject',
           'GeNNUserCodeObject']


# Don't generate any code for reading from/writing to arrays or
# variable declarations
class GeNNCodeGenerator(CPPCodeGenerator):

    def translate_to_read_arrays(self, statements):
        return []

    def translate_to_write_arrays(self, statements):
        return []

    def translate_to_declarations(self, statements):
        return []

    def translate_statement(self, statement):
        var, op, expr, comment = (statement.var, statement.op,
                                  statement.expr, statement.comment)
        # for debugging only: show translated statements
        print(var,op,expr,comment);
        if op == ':=':
            decl= self.c_data_type(statement.dtype) + ' '
            op = '='
        else:
            decl= ''
        code = decl + var + ' ' + op + ' ' + self.translate_expression(expr) + ';'
        if len(comment):
            code += ' // ' + comment
        return code


class GeNNCodeObject(CPPStandaloneCodeObject):
    templater = Templater('brian2genn', env_globals={'c_data_type': c_data_type})
    generator_class = GeNNCodeGenerator

class GeNNUserCodeObject(CPPStandaloneCodeObject):
    templater = Templater('brian2genn', env_globals={'c_data_type': c_data_type})
    generator_class = CPPCodeGenerator

codegen_targets.add(GeNNCodeObject)
codegen_targets.add(GeNNUserCodeObject)
