# FruitVision - System Overview

## 1. Introduction

FruitVision is an AI-powered fruit classification platform designed to allow users to upload fruit images and receive machine learning predictions.

The application combines:

- modern backend architecture;
- secure user authentication;
- database persistence;
- machine learning inference.

The goal of the project is to build a production-style AI application while demonstrating backend engineering principles.

---

## 2. Project Goals

FruitVision is designed to demonstrate competency in:

- Python backend development;
- FastAPI;
- PostgreSQL;
- SQLAlchemy ORM;
- database migrations;
- authentication systems;
- REST API design;
- machine learning integration.

The project is intentionally developed with production-quality practices rather than as a simple prototype.

---

## 3. High-Level User Flow

The intended user journey:

1. User creates an account.
2. User logs into the application.
3. User receives authentication credentials.
4. User uploads a fruit image.
5. Machine learning model analyzes the image.
6. Prediction result is stored.
7. User can view prediction history.

---

## 4. High-Level Architecture

FruitVision follows a layered backend architecture.

The request flow is:

Client

↓

FastAPI Router

↓

Service Layer

↓

Repository Layer

↓

PostgreSQL Database


Each layer has a specific responsibility.

---

## 5. Technology Stack

## Backend

- Python
- FastAPI

## Database

- PostgreSQL

## ORM

- SQLAlchemy 2.x

## Database Migration

- Alembic

## Authentication

- JWT
- Password hashing

## Machine Learning

- PyTorch
- Torchvision

---

## 6. Architectural Principles

The project follows these principles:

### Separation of Concerns

Each component has a clearly defined responsibility.

Examples:

- Routers handle HTTP communication.
- Services handle business logic.
- Repositories handle database operations.
- Models represent database entities.
- Schemas validate API data.

---

### Security First

The application avoids:

- storing plaintext passwords;
- using administrative database accounts;
- exposing sensitive information.

---

### Maintainability

The structure is designed so future features can be added without creating tightly coupled code.

---

## 7. Current Development Status

Current completed milestones:

- Project architecture setup
- PostgreSQL configuration
- SQLAlchemy setup
- Alembic migration setup
- User database model
- User registration
- Password hashing
- User login verification
- JWT token generation

Current milestone:

JWT authentication and protected routes.

---
