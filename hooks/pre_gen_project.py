import re
import sys
from cookiecutter.main import cookiecutter


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

package_name = "{{ cookiecutter.package_name|lower|replace('-', '_') }}"

if not re.match(MODULE_REGEX, package_name):
    print('ERROR: %s is not a valid Python module name!' % package_name)

    # exits with status 1 to indicate failure
    sys.exit(1)
