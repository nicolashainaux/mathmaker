To add a new test section :

- go to the right directory, create a blank ****_test.py,
  copy the (simple) structure from model_test.py
- add the matching import in the __init__.py file from the directory
  where your ****_test.py is located
- add the ("name", path.to.the.****_test) in the AVAILABLE_UNITS list
  from autotest/__init__.py
- fill it with objects to be tested plus the check tests...
