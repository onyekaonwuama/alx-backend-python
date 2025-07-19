# 0x03. Unittests and Integration Tests

## Description

This project focuses on writing **unit tests** and **integration tests** in Python using the `unittest` framework, with additional tools such as `parameterized` and `mock`. You will learn how to create test cases for functions and classes, mock dependencies to isolate test scenarios, and differentiate between unit and integration tests.

## Learning Objectives

By the end of this project, you will be able to:

- Explain the difference between unit and integration tests.
- Apply common testing patterns including:
  - Mocking
  - Parameterization
  - Fixtures
- Execute Python tests using the `unittest` module.
- Use `unittest.mock` to replace parts of your system under test and make assertions about how they were used.

## Requirements

- Python 3.7
- Ubuntu 18.04 LTS
- Code must comply with **pycodestyle** (version 2.5).
- All files must be executable.
- All modules, classes, and functions must include comprehensive documentation.
- All functions and coroutines must include type annotations.
- A `README.md` file is mandatory.

## Resources

- [`unittest`](https://docs.python.org/3/library/unittest.html) — Unit testing framework
- [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html) — Mock object library
- [parameterized](https://github.com/wolever/parameterized)
- [How to mock a readonly property with mock?](https://stackoverflow.com/questions/24836205/how-to-mock-a-readonly-property-with-mock)
- Memoization concepts

## Project Structure

```bash
.
├── client.py
├── fixtures.py
├── test_client.py
├── test_utils.py
├── utils.py
└── README.md
