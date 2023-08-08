# Developer documentation: Running C coverage locally

Python test coverage is checked automatically by the CI workflow, but the C
coverage was unable to be successfully configured in the same way. To run the
C coverage check locally, use the following steps (all commands should be executed
from your bash shell in the root `pypolyclip` directory):

1. Make sure that the [test] dependencies are installed (`pip install .[test]`).
2. Run the following preparatory commands:

    export CFLAGS="--coverage"\
    export CC=gcc\
    rm -rf build/temp.* \
    rm -rf build/lib.*

3. Rebuild the pypolyclip C extension:

    python setup.py build_ext --inplace --force

4. Run the python tests (`pytest`).

    pytest

5. Remove any existing coverage files and run `gcovr` to generate the C coverage report:

    rm -rf coverage\
    mkdir coverage\
    gcovr --filter pypolyclip/src/ --print-summary --html-details coverage/index.html

This will print out a summary of the coverage to your terminal as well as generating html
reports in the `coverage` directory.
