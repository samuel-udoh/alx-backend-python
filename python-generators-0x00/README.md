# Advanced Python & MySQL: A Generator-Based Toolkit

This project is a practical demonstration of advanced Python techniques for interacting with a MySQL database. The primary focus is on writing memory-efficient, scalable, and robust data processing scripts using **Python generators**.

The scripts cover a range of common and important database tasks, from initial database seeding to complex data streaming, pagination, and aggregation, all while adhering to best practices for security and performance.

## Features

-   **Secure Database Seeding:** Populates a MySQL database from a CSV file using environment variables for credentials.
-   **Efficient Batch Inserts:** Uses `cursor.executemany()` for high-performance data insertion.
-   **Lazy Data Streaming:** Implements a generator to stream data row-by-row, keeping memory usage minimal.
-   **Database Pagination:** Demonstrates a lazy-loading pagination system using `LIMIT` and `OFFSET`.
-   **Memory-Efficient Aggregation:** Calculates aggregate functions (like average) on a large dataset without loading it all into memory.
-   **Robust Connection Management:** Employs `try...finally` blocks to ensure database connections are always closed properly.
-   **Demonstration of Cursor Types:** Implicitly showcases the difference and use cases for buffered vs. unbuffered cursors.

## Prerequisites

Before you begin, ensure you have the following installed and running:
-   **Python 3.8+:** Installed within your WSL environment.
-   **pip:** The Python package installer.
-   **MySQL Server:** Installed and running on your WSL instance.

## Setup & Installation

Follow these steps to get the project running on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and Activate a Virtual Environment (Recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    A `requirements.txt` file should be in the project root. Install all necessary packages with:
    ```bash
    pip install -r requirements.txt
    ```
    If you don't have one, create `requirements.txt` with the following content:
    ```
    mysql-connector-python
    python-dotenv
    ```

4.  **Set Up Environment Variables**
    This project uses a `.env` file to securely manage database credentials. Create a file named `.env` in the project root by copying the example:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your MySQL credentials:
    ```ini
    # .env
    DB_HOST=localhost
    DB_USER=your_mysql_user
    DB_PASSWORD=your_mysql_password
    ```

5.  **Prepare the Data File**
    Ensure you have the `user_data.csv` file in the project root. The script `0-main.py` will use this file to seed the database.

## Running the Scripts

Make sure your scripts are executable:
```bash
chmod +x *.py
```

### 1. `0-main.py` - Database Setup and Seeding
This is the first script you should run. It connects to MySQL, creates the `ALX_prodev` database and the `user_data` table, and then populates it with data from `user_data.csv`.

**To Run:**
```bash
./0-main.py
```
**Expected Output:**
```
--- Starting Database Seeding Script ---
Successfully connected to MySQL server.
Database 'ALX_prodev' is ready.
Successfully connected to database 'ALX_prodev'.
Table 'user_data' is ready.
Successfully inserted 1000 rows.
Database connection closed.
--- Script finished. ---
```

### 2. `1-main.py` - Streaming a Subset of Users
This script demonstrates how to use a generator (`stream_users`) to fetch data row-by-row and how to consume only a small part of that stream using `itertools.islice`.

**To Run:**
```bash
./1-main.py
```
**Expected Output:** (Will print the first 6 users from the database)
```
Connected to ALX_prodev
('uuid-string-1', 'User Name 1', 'email1@example.com', Decimal('...'))
('uuid-string-2', 'User Name 2', 'email2@example.com', Decimal('...'))
... (4 more users)
Database connection closed.
```

### 3. `2-main.py` - Lazy Pagination
This script showcases a powerful pagination pattern where pages of data are only fetched from the database when they are explicitly requested.

**To Run:**
```bash
./2-main.py
```
**Expected Output:**
```
Starting lazy pagination with page size 10...

--- Requesting Page 1 ---
Received Page 1 with 10 users.

--- Requesting Page 2 ---
Received Page 2 with 10 users.

--- Requesting remaining pages with a for loop ---
Received Page 3 with 10 users.
...
--- No more pages to fetch. Generator is finished. ---
```

### 4. `3-main.py` - Memory-Efficient Aggregation
This script calculates the average age of all users in the database without ever loading more than one user's age into memory at a time. It's a prime example of why generators are essential for big data tasks.

**To Run:**
```bash
./3-main.py
```
**Expected Output:**
```
Connected to ALX_prodev
Database connection closed.
Average age of users: 54.82
```

## Key Concepts Demonstrated

-   **Generators for Lazy Loading:** Instead of returning a massive list of data, functions use `yield` to create a generator. The generator produces one item (or one page) at a time, only when asked. This is the core principle behind `stream_users` and `lazy_paginate`.

-   **Memory-Efficient Processing:** The average age calculation in `3-main.py` is the ultimate demonstration of this. It processes a potentially huge dataset with a tiny, constant memory footprint by keeping a running total instead of storing all the data.

-   **Buffered vs. Unbuffered Cursors:** The "Unread result found" error we encountered highlights a crucial concept.
    -   **Unbuffered (Default):** Streams results from the server. The connection is busy until all results are read. Ideal for huge datasets when you process *every* row.
    -   **Buffered (`buffered=True`):** Downloads all results to the client's memory at once, freeing the connection. This is **necessary** when you need to stop reading part-way through a result set (e.g., when using `islice`).

-   **Producer-Consumer Pattern:** The scripts are structured so that one function "produces" data (e.g., `stream_users_in_batches`) and another "consumes" it (e.g., `batch_processing`). This separation makes code cleaner, more reusable, and easier to test.