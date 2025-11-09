# Python Generators — ALX Backend Project

## 🧠 Overview
This project demonstrates the use of **Python generators** to handle large datasets efficiently, implement batch processing, lazy loading, and compute memory-efficient aggregates.  

It integrates with a MySQL database to simulate real-world backend operations such as streaming, pagination, and aggregation — all while maintaining optimal performance.

---

## 🧩 Tasks Breakdown

### **Task 0 — seed.py**
- Connects to MySQL.
- Creates database `ALX_prodev` and table `user_data`.
- Loads data from `user_data.csv` into the database.

### **Task 1 — 0-stream_users.py**
- Implements a generator `stream_users()` that streams rows one by one using `yield`.

### **Task 2 — 1-batch_processing.py**
- Fetches and processes users in batches using generators.
- Filters users older than 25 and prints them.
- Avoids using `return` statements to satisfy project checks.

### **Task 3 — 2-lazy_paginate.py**
- Implements a generator `lazy_pagination(page_size)` to simulate fetching paginated data.

### **Task 4 — 4-stream_ages.py**
- Streams user ages from the database one by one.
- Calculates and prints the average age efficiently without loading all data into memory.

---

## ⚙️ Setup Instructions
1. Ensure you have **MySQL** and **Python 3.x** installed.
2. Create a `user_data.csv` file with sample user data (name, email, age).
3. Run:
   ```bash
   python3 seed.py
