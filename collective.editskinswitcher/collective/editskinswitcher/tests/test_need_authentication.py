import unittest
from Testing import ZopeTestCase as ztc
from base import BaseTestCase


def test_suite():
    return unittest.TestSuite([

        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'need_authentication.txt', package='collective.editskinswitcher.tests',
            test_class=BaseTestCase),
        
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')