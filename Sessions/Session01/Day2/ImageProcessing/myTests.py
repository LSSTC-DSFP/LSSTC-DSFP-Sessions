#!/usr/bin/env ipython
import sys, unittest
import numpy as np

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class DotTestCase(unittest.TestCase):
    """A test fixture for numpy's dot products"""

    def setUp(self):
        """Establish our fixture"""
        n = 4
        self.x = np.arange(n)
        self.y = 1 - np.linspace(0.0, 1.0, n)

    def tearDown(self):
        """Cleanup"""
        del self.x
        del self.y

    def testDotI(self):
        """Test np.dot for x.x"""
        self.assertEqual(np.dot(self.x, self.x),
                         sum([x*x for x in self.x]))

class DetectionTestCase(unittest.TestCase):
    """A test fixture for numpy's dot products"""

    def setUp(self):
        """Establish our fixture"""
        pass

    def tearDown(self):
        """Cleanup"""
        pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def suite():
    """Returns a suite containing all the test cases in this module."""
    suites = []
    suites += unittest.makeSuite(DotTestCase)
    suites += unittest.makeSuite(DetectionTestCase)
    return unittest.TestSuite(suites)

def run(shouldExit=False):
    """Run the tests"""

    if shouldExit:
        unittest.main()
    else:
        return unittest.TextTestRunner().run(suite()).wasSuccessful()

if __name__ == "__main__":
    run(True)
