"""Add "test" action for the "gepetuto" program."""

import logging
from collections import defaultdict
from pathlib import Path
from subprocess import check_call

LOG = logging.getLogger("gepetuto.test")


def test(files, **kwargs):
    """Test python scripts."""
    python_interpreter = kwargs["python"]
    LOG.info("testing tutorial sources.")
    for tp_files in files.values():
        for tp_file in tp_files:
            LOG.debug("Checking %s", tp_file)
            check_call([python_interpreter, tp_file])
    ipynbs = get_ipynbs(files)
    for tp_ipynbs in ipynbs.values():
        for tp_ipynb in tp_ipynbs:
            check_ipynb(tp_ipynb, python_interpreter)
    LOG.info("test passed.")


def get_ipynbs(files):
    """Get the dictionary of ipynbs to test."""
    ipynbs = defaultdict(list)
    for ipynb in Path().glob("*.ipynb"):
        prefix = str(ipynb).split("-")[0]
        if prefix.isdecimal():
            if int(prefix) in files.keys():
                ipynbs[prefix].append(ipynb)
        else:
            ipynbs[prefix].append(ipynb)
    return ipynbs


def check_ipynb(ipynb, python_interpreter):
    """Check .ipynb files from given tp_number."""
    check_call(["jupyter", "nbconvert", "--to", "script", f"{ipynb}"])
    prefix = str(ipynb).split("-")[0]
    converted_ipynb = next(Path().glob(f"{prefix}-*.py"))
    LOG.debug("Checking temporary file %s", converted_ipynb)
    check_call([python_interpreter, converted_ipynb])
    Path.unlink(converted_ipynb)
