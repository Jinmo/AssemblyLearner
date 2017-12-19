#!/usr/bin/python

tests = [
    'compiler'
]

print('Running tests...')

for test in tests:
    testModule = getattr(__import__('tests.' + test), test)
    testModule.run()
