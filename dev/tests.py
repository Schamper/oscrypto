# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import unittest
import re
import sys

if sys.version_info < (3,):
    range = xrange  # noqa
    from cStringIO import StringIO
else:
    from io import StringIO

from tests import test_classes


def run(matcher=None, repeat=1):
    """
    Runs the tests

    :param matcher:
        A unicode string containing a regular expression to use to filter test
        names by. A value of None will cause no filtering.

    :param repeat:
        An integer - the number of times to run the tests

    :return:
        A bool - if the tests succeeded
    """

    loader = unittest.TestLoader()
    # We have to manually track the list of applicable tests because for
    # some reason with Python 3.4 on Windows, the tests in a suite are replaced
    # with None after being executed. This breaks the repeat functionality.
    test_list = []
    for test_class in test_classes():
        if matcher:
            names = loader.getTestCaseNames(test_class)
            for name in names:
                if re.search(matcher, name):
                    test_list.append(test_class(name))
        else:
            test_list.append(loader.loadTestsFromTestCase(test_class))

    stream = sys.stdout
    verbosity = 1
    if matcher and repeat == 1:
        verbosity = 2
    elif repeat > 1:
        stream = StringIO()

    for _ in range(0, repeat):
        suite = unittest.TestSuite()
        for test in test_list:
            suite.addTest(test)
        result = unittest.TextTestRunner(stream=stream, verbosity=verbosity).run(suite)

        if len(result.errors) > 0 or len(result.failures) > 0:
            if repeat > 1:
                print(stream.getvalue())
            return False

        if repeat > 1:
            stream.truncate(0)

    return True
