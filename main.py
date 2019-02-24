import re
import os
#Get file as cmd argument later
    #Handle errors( doesnt exist, isnt .cs or something else)
#Parse file and get all the fields
    #Find all the lines matching private/public readonly Type _name;
    #Named convention helps a lot I guess
#Generate Mock fields and initialize the from setup
#Add correct boilerplate stuff

service_file_path="ExampleService.cs"

def generate_unit_test_file(service_file_path):
    unit_test_name=generate_unit_test_name(service_file_path)
    injected_dependencies=get_injected_dependencies()
    mocked_declarations=generate_mocked_declarations(injected_dependencies)  

    for x in mocked_declarations:
        print(x)

    setup_method=generate_setup_method(mocked_declarations)

    print(unit_test_name)  
    
def get_injected_dependencies():
    injected_dependencies=[]
    for line in open(service_file_path, 'r'):
        if (is_injected_dependency(line)):
            injected_dependencies.append(line)
    return injected_dependencies

def is_injected_dependency(line):
    line=line.strip()
    return re.search('private[\s]readonly[\s][^ ]+[\s]_[^ ;]+;',line)

def generate_mocked_declarations(injected_dependencies):
    mocked_declarations=[]

    for injected_dependency in injected_dependencies:
        statement_segments=injected_dependency.split()
        statement_segments[2]=f'Mock<{statement_segments[2]}>'

        mocked_declarations.append(' '.join(statement_segments))
    return mocked_declarations


def generate_unit_test_name(service_file_path):
    service_name=os.path.basename(os.path.normpath(service_file_path))
    return service_name[:-3] + 'Tests' + service_name[-3:]

def generate_setup_method(mocked_declarations):
    lines=[]
    lines.append('[SetUp]')
    lines.append('public void SetUp()')
    lines.append('{')

    for declaration in mocked_declarations:
        statement_segments=declaration.split()
        dependency_name=statement_segments[-1][:-1]
        print(dependency_name)

        lines.append(f'')

    return '\n'.join(lines);
generate_unit_test_file(service_file_path)