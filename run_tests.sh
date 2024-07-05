#!/bin/bash

# Run the tests using unittest discover
python -m unittest discover -s tests -p "test_*.py"

# Check the exit status of unittest
if [ $? -eq 0 ]; then
  echo "Tests passed successfully!"
else
  echo "Tests failed."
fi

