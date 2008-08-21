import unittest
import doctest

from Testing import ZopeTestCase as ztc
from collective.editskinswitcher.tests import base

import zope.component.testing
import zope.component.eventtesting


def test_suite():
    return unittest.TestSuite([

        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'tests/property_edit.txt', package='collective.editskinswitcher',
            test_class=base.BaseFunctionalTestCase),
        
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
