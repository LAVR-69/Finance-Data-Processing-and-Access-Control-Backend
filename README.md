# Finance Data Processing and Access Control Backend

## Overview

This project is a backend system built for managing financial records with role-based access control.

It allows users to create, update, delete, and analyze financial data such as income and expenses, while enforcing permissions based on user roles.

---

## Features

* User role management (Admin, Viewer, Analyst)
* Financial record CRUD operations
* Filtering by type, category, and date
* Dashboard analytics (total income, expenses, balance)
* Category-wise summaries
* Recent activity tracking
* Role-based access control (RBAC)
* Input validation and error handling

---

## Tech Stack

* Python (Flask)
* GraphQL (Ariadne)
* PostgreSQL
* Docker

---

## Queries

### Get Records

```graphql
{
  records(type: "income") {
    amount
    category
  }
}
```

### Add Record

```graphql
mutation {
  addRecord(
    amount: 1000,
    type: "income",
    category: "salary",
    date: "2026-04-03",
    note: "test",
    user: "Aviral"
  ) {
    id
  }
}
```

### Response
```graphsql
{
  "data": {
    "addRecord": {
      "id": 17
    }
  }
}
```

### Summary

```graphql
{
  summary {
    totalIncome
    totalExpense
    balance
  }
}
```

### Response

```graphql
{
  "data": {
    "summary": {
      "balance": 69000,
      "totalExpense": 0,
      "totalIncome": 69000
    }
  }
}
```

### Recent Records

```graphql
{
  recentRecords(limit: 3) {
    id
    amount
  }
}
```

### Response

```graphql
{
  "data": {
    "recentRecords": [
      {
        "amount": 1000,
        "id": 17
      },
      {
        "amount": 1000,
        "id": 16
      },
      {
        "amount": 1000,
        "id": 15
      }
    ]
  }
}

---

### Setup Instructions
```

1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/Finance-Data-Processing-and-Access-Control-Backend.git
cd Finance-Data-Processing-and-Access-Control-Backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run PostgreSQL using Docker:

```bash
docker run --name postgres-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=finance_db \
  -p 5432:5432 \
  -d postgres
```

4. Run the backend:

```bash
python app.py
```

5. Open GraphQL:

```
https://127.0.0.1:5000/graphql
```

---

## Access Control

* Admin → Full access (create, update, delete)
* Analyst → View records and analytics
* Viewer → Read-only access

---

## Design Decisions

* Used GraphQL for flexible data querying
* Implemented parameterized queries to prevent SQL injection
* Used PostgreSQL for reliable data persistence
* Designed modular and clean resolver logic

---

## Limitations

* No authentication system (JWT)
* No pagination
* Basic error handling

---

## Future Improvements

* Add authentication (JWT)
* Add pagination
* Improve logging and monitoring
