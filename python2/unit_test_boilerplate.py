#!/usr/bin/env python
# Corey Goldberg
#
#  Python unit tests - boilerplate/sample
#
#  http://docs.python.org/library/unittest.html
#



import unittest
import my_module



def main():
    test_cases = [
        TestFoo, 
        TestBar, 
    ]
        
    test_suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    all_tests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
    
    
    
class TestFoo(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_x(self):
        value = my_module.x()
        self.assertTrue('foo' in value, value)
        
    def test_y(self):
        value = my_module.y()
        self.assertEqual(value, 1.0, value)
        
    def tearDown(self):
        pass



class TestBar(unittest.TestCase):    
    def test_z(self):
        value = my_module.z()
        self.assertTrue(value, value)
        


if __name__ == '__main__':
    main()
    

