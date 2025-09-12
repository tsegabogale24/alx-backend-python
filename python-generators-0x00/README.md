# Python Generators Project – ALX Backend

## Project Overview

This project demonstrates **advanced Python techniques** by using **generators** to stream rows from a MySQL database efficiently. It includes:

- Setting up a MySQL database (`ALX_prodev`)
- Creating a table `user_data`
- Populating the table from a CSV file
- Streaming rows lazily using a **generator**

Generators allow processing large datasets **without loading all data into memory**, making the project memory-efficient and scalable.

---

## Files in this Repository

| File | Description |
|------|-------------|
| `seed.py` | Python script that handles database connection, table creation, data insertion, and a generator to stream rows |
| `user_data.csv` | Sample data for the `user_data` table |
| `README.md` | Project documentation |

---

## Requirements

- Python 3.x
- MySQL Server
- Python packages:
  ```bash
  pip install mysql-connector-python
