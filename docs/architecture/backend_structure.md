# FruitVision Backend Structure

## 1. Overview

FruitVision follows a layered backend architecture designed to separate responsibilities and keep the application maintainable as it grows.

The backend is organized around the following layers:

Client

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

Database


Each layer has a specific responsibility and should avoid taking responsibility away from another layer.

---

# 2. Backend Directory Structure

The main application structure:


app/

├── api/
├── services/
├── repositories/
├── models/
├── schemas/
├── core/
├── db/
└── ai/


---

# 3. API Layer

Location:


app/api/


## Responsibility

The API layer handles communication between external clients and the application.

It contains FastAPI routers.

Examples:

- authentication routes;
- user routes;
- prediction routes.

Example endpoints:


POST /auth/register

POST /auth/login

GET /users/me

POST /predict


---

## What belongs here

The API layer should handle:

- receiving HTTP requests;
- validating incoming data;
- calling services;
- returning responses.

---

## What should NOT happen here

Routers should not:

- directly query the database;
- hash passwords;
- contain complex business rules;
- perform machine learning inference.

Example:

Bad:


Router
|
├── Query database
├── Hash password
└── Create user


Better:


Router

↓

Service

↓

Repository


---

# 4. Service Layer

Location:


app/services/


## Responsibility

The service layer contains business logic.

It answers:

"What should happen when a user performs an action?"

Examples:

Authentication service:

- register user;
- validate credentials;
- create authentication tokens.

Prediction service:

- process uploaded image;
- call AI model;
- store prediction result.

---

## Why services exist

Without services, routers become overloaded.

Example:

A registration request involves:

1. Checking if email exists.
2. Hashing password.
3. Creating a user.
4. Saving to database.

These are business rules, not HTTP concerns.

The service layer coordinates these actions.

---

# 5. Repository Layer

Location:


app/repositories/


## Responsibility

Repositories handle database communication.

They provide an abstraction over database operations.

Examples:


create_user()

get_user_by_email()

get_user_by_id()

save_prediction()

get_prediction_history()


---

## Why repositories exist

Without repositories, database queries would appear everywhere.

Example:


Router
Service
Prediction Endpoint
Admin Endpoint

    |
    v

Multiple database queries everywhere


Repositories create a single place responsible for persistence.

---

# 6. Models

Location:


app/models/


## Responsibility

Models define database tables using SQLAlchemy.

They describe:

- table names;
- columns;
- relationships.

Example:

User model:


users table

id
username
email
hashed_password
created_at
updated_at


---

Models represent database structure.

They are not used for API validation.

---

# 7. Schemas

Location:


app/schemas/


## Responsibility

Schemas define the shape of data entering and leaving the API.

They use Pydantic.

Examples:

Request:


UserCreate

LoginRequest


Response:


UserResponse

TokenResponse


---

## Models vs Schemas

Models:


Database representation


Schemas:


API representation


Example:

Database user:


User Model

id
username
email
hashed_password


API response:


UserResponse

id
username
email


The password should never leave the backend.

---

# 8. Core Layer

Location:


app/core/


## Responsibility

The core layer contains application-wide functionality.

Examples:


config.py

security.py


---

## config.py

Responsible for application settings.

Examples:

- database URL;
- JWT secret;
- token expiration.

The application reads configuration from environment variables.

Flow:


.env

↓

config.py

↓

Application


---

## security.py

Responsible for security operations.

Examples:

- password hashing;
- password verification;
- JWT token creation;
- JWT token decoding.

Security logic should not be duplicated throughout the application.

---

# 9. Database Layer

Location:


app/db/


## Responsibility

The database layer manages SQLAlchemy configuration.

Examples:


database.py

session.py

base.py


---

## database.py

Creates the SQLAlchemy engine.

The engine represents the connection between the application and PostgreSQL.

---

## session.py

Manages database sessions.

A session represents a single conversation with the database.

Example:

A request comes in:


Create user

↓

Open database session

↓

Perform operation

↓

Close session


---

## base.py

Contains the SQLAlchemy Base class.

Models inherit from this Base.

Example:


class User(Base):


Alembic uses:


Base.metadata


to understand database structure.

---

# 10. AI Layer

Location:


app/ai/


## Responsibility

Contains machine learning functionality.

Examples:


model_loader.py

predict.py

preprocessing.py


The AI layer should only handle:

- loading models;
- preparing images;
- running inference.

It should not handle:

- authentication;
- database operations;
- HTTP requests.

---

# 11. Feature Development Flow

When adding a new feature, follow this pattern:

Example:

Adding fruit prediction.

## API

Create:


app/api/predictions.py


Handles:


POST /predict


---

## Service

Create:


app/services/predictions.py


Handles:

- image processing;
- prediction logic;
- business rules.

---

## Repository

Create:


app/repositories/predictions.py


Handles:

- saving predictions;
- retrieving history.

---

## Model

Create:


app/models/prediction.py


Defines:


predictions table


---

## Schema

Create:


app/schemas/predictions.py


Defines:

- request format;
- response format.

---

# Summary

FruitVision uses a layered architecture where:

API layer:
Handles HTTP communication.

Service layer:
Handles business logic.

Repository layer:
Handles database operations.

Models:
Represent database tables.

Schemas:
Represent API data.

Core:
Contains shared application functionality.

Database layer:
Manages database connectivity.

AI layer:
Contains machine learning functionality.

This separation allows FruitVision to grow while keeping the codebase understandable and maintainable.