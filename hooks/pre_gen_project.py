"""Script run before porject generation."""

import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

package_name = "{{ cookiecutter.module_name }}"

if not re.match(MODULE_REGEX, package_name):
    print('ERROR: %s is not a valid Python module name!' % package_name)

    # exits with status 1 to indicate failure
    sys.exit(1)
