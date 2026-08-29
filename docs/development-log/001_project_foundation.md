# Development Log 001: Project Foundation

## Date

August 2026

---

# Objective

Establish the foundation of FruitVision as a production-style backend application.

The goal was not simply to create a working prototype, but to build an application that demonstrates professional software engineering practices.

---

# Project Vision

FruitVision is an AI-powered fruit classification platform.

The application allows users to:

1. Create an account.
2. Authenticate securely.
3. Upload fruit images.
4. Receive machine learning predictions.
5. Store and retrieve prediction history.

The project combines backend engineering and machine learning.

---

# Initial Engineering Goals

The project was designed to demonstrate competency in:

- Python backend development;
- FastAPI;
- PostgreSQL;
- SQLAlchemy;
- Alembic migrations;
- authentication systems;
- REST API design;
- machine learning integration;
- production deployment practices.

---

# Why FastAPI Was Chosen

FastAPI was selected because it provides:

- modern Python backend development;
- automatic API documentation;
- strong integration with Pydantic;
- asynchronous capabilities;
- type-hint driven development.

FastAPI also provides a structure that encourages clean API design.

---

# Why PostgreSQL Was Chosen

PostgreSQL was selected as the primary database because:

- it is widely used in production systems;
- it supports complex relational data;
- it integrates well with SQLAlchemy;
- it provides reliability and scalability.

FruitVision requires relational data because users and predictions have relationships.

Example:


One User

|

Many Predictions


---

# Initial Architecture Decision

A layered architecture was chosen.

The application follows:


API Layer

↓

Service Layer

↓

Repository Layer

↓

Database


---

# Reason for Layered Architecture

The main motivation was separation of concerns.

Without separation:

- routes become too large;
- database logic spreads everywhere;
- business rules become difficult to maintain.

With separation:

API:
Handles HTTP communication.

Services:
Handle business logic.

Repositories:
Handle database operations.

---

# Why AI Development Was Delayed

A major architectural decision was to delay machine learning integration.

The initial temptation was:


Train model

↓

Create prediction endpoint


However, production applications require supporting infrastructure first.

The decision was made to build:

1. Database foundation.
2. Authentication.
3. API structure.
4. User management.

before integrating AI.

---

# Initial Project Structure

The application was organized as:


app/

├── api/
├── services/
├── repositories/
├── models/
├── schemas/
├── core/
├── db/
└── ai/


Each layer has a defined responsibility.

---

# Key Lessons

During this phase, the following engineering concepts were introduced:

## Separation of Concerns

Different parts of the application should have different responsibilities.

---

## Production Mindset

The project was approached as an application that could eventually support real users.

---

## Avoiding Tutorial-Driven Development

The objective was not only to copy code but understand:

- why decisions are made;
- what problems patterns solve;
- how systems evolve.