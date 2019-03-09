import re,os,sys

def validate_input_parameter(file_path):
    if(not os.path.exists(file_path)):
        raise ValueError("File path:\""+file_path+"\"does not exist!")


def generate_unit_test_file(service_file_path):
    validate_input_parameter(file_path)
    service_name = os.path.basename(os.path.normpath(service_file_path))[:-3]
    unit_test_name = generate_unit_test_name(service_file_path)
    injected_dependencies = get_injected_dependencies(service_file_path)
    mocked_declarations = generate_mocked_declarations(injected_dependencies)
    setup_method_statements = generate_setup_method(mocked_declarations, service_name)

    with open(unit_test_name, "w") as f:
        f.write('using FluentAssertions;\nusing NUnit.Framework;\nusing System.Collections.Generic;\nusing Moq;\n\n')
        f.write('namespace InsertProjectNameHere.Tests\n{\n')
        f.write('\t[TestFixture]\n')
        f.write(f'\tpublic class {unit_test_name[:-3]}\n')
        f.write('\t{\n')
        for declaration in mocked_declarations:
            f.write(f'\t\t{declaration}\n')
        f.write('\n')
        f.write(f'\t\tprivate {service_name} _service;\n\n')
        for statement in setup_method_statements:
            f.write(f'\t\t{statement}\n')
        f.write('\t}\n}')


def get_injected_dependencies(service_file_path):
    injected_dependencies = []
    for line in open(service_file_path, 'r'):
        if (is_injected_dependency(line)):
            injected_dependencies.append(line)
    return injected_dependencies


def is_injected_dependency(line):
    line = line.strip()
    return re.search(r'private[\s]readonly[\s][^ ]+[\s]_[^ ;]+;', line)


def generate_mocked_declarations(injected_dependencies):
    mocked_declarations = []

    for injected_dependency in injected_dependencies:
        statement_segments = injected_dependency.split()
        statement_segments[2] = f'Mock<{statement_segments[2]}>'
        statement_segments.remove('readonly')

        mocked_declarations.append(' '.join(statement_segments))
    return mocked_declarations


def generate_unit_test_name(service_file_path):
    service_name = os.path.basename(os.path.normpath(service_file_path))
    return service_name[:-3] + 'Tests' + service_name[-3:]


def generate_setup_method(mocked_declarations, service_name):
    lines = []
    lines.append('[SetUp]')
    lines.append('public void SetUp()')
    lines.append('{')

    for declaration in mocked_declarations:
        statement_segments = declaration.split()
        dependency_name = statement_segments[-1][:-1]
        mocked_declaration_type = statement_segments[1]

        lines.append(f'\t{dependency_name} = new {mocked_declaration_type}();')

    constructor_statement = generate_constructor_statement(service_name,mocked_declarations)
    "constructor:"+constructor_statement
    lines.append(f'\n\t\t\t{constructor_statement}')
    lines.append('}')
    return lines


def generate_constructor_statement(service_name,mocked_declarations):
    parameters = []
    for declaration in mocked_declarations:
        declaration_segments = declaration.split()
        dependency_name = declaration_segments[-1][:-1]
        parameters.append(f'{dependency_name}.Object')

    comma_separated_parameters = ','.join(parameters)
    return f'_service = new {service_name}({comma_separated_parameters});'

if(sys.argv.__len__()<2):
    print(".cs file should be provided as argument.")
else:
    file_path = sys.argv[1]

    try:
        generate_unit_test_file(file_path)
    except ValueError as error:
        print(error)
