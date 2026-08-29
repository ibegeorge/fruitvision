# Development Log 002: Database Foundation

## Objective

Establish a reliable database foundation for FruitVision.

The goal was to connect the FastAPI application to PostgreSQL using production-oriented practices.

This involved:

- PostgreSQL setup;
- database user creation;
- SQLAlchemy configuration;
- database session management;
- Alembic migrations.

---

# PostgreSQL Setup

## Initial Approach

During early development, the application was initially tested using the default PostgreSQL role created during local installation.

This worked for local experimentation, but it does not represent a production-quality setup.

---

# Database User Separation Decision

## Problem

Applications should not connect to databases using administrator accounts.

Using a highly privileged database user creates unnecessary security risks.

If the application credentials are compromised, the attacker gains excessive database access.

---

## Decision

A dedicated application database user was created.

Database:


fruitvision


Application user:


fruitvision_user


The application connects using this user rather than the PostgreSQL administrator account.

---

## Reasoning

This approach follows the principle of least privilege.

The application only receives the permissions required to operate its own database.

This more closely resembles real production environments.

---

# SQLAlchemy Integration

## Why SQLAlchemy Was Introduced

SQLAlchemy acts as the bridge between Python objects and relational database tables.

Instead of manually writing SQL queries everywhere, SQLAlchemy allows the application to work with Python classes.

Example:

Python:


User class


represents:


users table


in PostgreSQL.

---

# Database Layer Structure

The database configuration was organized as:


app/db/

├── database.py
├── session.py
└── base.py


---

# database.py

## Responsibility

Creates the SQLAlchemy engine.

The engine represents the connection between the application and PostgreSQL.

Flow:


FastAPI Application

    |

    v

SQLAlchemy Engine

    |

    v

PostgreSQL


---

# session.py

## Responsibility

Manages database sessions.

A session represents a single interaction with the database.

Example:


HTTP Request

    |

    v

Open Database Session

    |

    v

Perform Database Operations

    |

    v

Close Session


---

# base.py

## Responsibility

Contains the SQLAlchemy Base class.

All database models inherit from this Base.

Example:

```python
class User(Base):

The Base object also provides metadata.

This metadata allows migration tools to understand the application's database structure.

Alembic Introduction
Problem

When database structures change, manually writing SQL migrations becomes difficult.

Example:

Initial database:

users

id
email
password

Later:

users

id
email
password
created_at
updated_at

The database needs to evolve.

Solution

Alembic was introduced as the database migration tool.

The relationship:

SQLAlchemy Models

        |

        v

Alembic Migration

        |

        v

PostgreSQL Schema
How Alembic Works

The developer defines database structure using SQLAlchemy models.

Example:

class User(Base):
    __tablename__ = "users"

Alembic compares:

Current database state

against

Model metadata

and generates migration instructions.

Instead of manually writing:

CREATE TABLE users (...);

Alembic generates and applies the migration.

Migration Workflow

The development workflow becomes:

Modify SQLAlchemy models.
Generate migration:
alembic revision --autogenerate
Review migration file.
Apply migration:
alembic upgrade head
Database Design Philosophy

The database was designed around the application's future requirements.

The initial entities planned:

User

Stores:

account information;
authentication details.

Example:

id
username
email
hashed_password
created_at
updated_at
Prediction

Future table.

Stores:

uploaded image;
predicted fruit;
confidence score;
timestamp.

Relationship:

User

 |

Many Predictions

