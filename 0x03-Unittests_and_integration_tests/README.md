# Unit and Integration Tests - Python

This project is part of the **ALX Backend Python** track.  
It covers writing **unit tests** and **integration tests** using the Python `unittest` framework and `parameterized` for test expansion.

---

##  Learning Objectives

- Understand the purpose of **unit tests** and **integration tests**.
- Write effective test cases using the `unittest` module.
- Use the `parameterized` package to simplify repetitive tests.
- Mock external calls and dependencies with `unittest.mock`.
- Structure tests for better readability and maintainability.

---

## 🛠️ Project Structure

0x03-Unittests_and_integration_tests/
│── test_utils.py # Unit tests for utils.py functions
│── utils.py # Utility functions being tested
│── README.md # Project documentation


---

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/alx-backend-python.git
   cd alx-backend-python/0x03-Unittests_and_integration_tests
(Optional) Create and activate a virtual environment:


python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:

pip install -r requirements.txt
🧪 Running Tests
Run all tests with:
python -m unittest discover
Run a specific test file:


python -m unittest test_utils.py
 Tasks Completed
0. Parameterize a unit test
Implemented TestAccessNestedMap.test_access_nested_map using @parameterized.expand.

Tested multiple input scenarios for access_nested_map.

1. Parameterize a unit test (exception handling)
Implemented TestAccessNestedMap.test_access_nested_map_exception.

Verified that KeyError is raised for invalid paths.

📌 Notes
The access_nested_map function retrieves values from nested dictionaries using a path (tuple).

Unit tests ensure correctness for both valid lookups and invalid cases.
