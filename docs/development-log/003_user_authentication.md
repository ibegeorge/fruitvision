# Development Log 003: User Authentication

## Objective

Implement a secure authentication foundation for FruitVision.

The authentication system allows users to:

- create accounts;
- securely store credentials;
- verify login credentials;
- prepare the application for protected user-specific features.

Authentication was implemented before machine learning integration because user identity is foundational to the rest of the application.

---

# Authentication Architecture

The authentication flow follows the layered architecture:

Client

↓

API Router

↓

Authentication Service

↓

User Repository

↓

PostgreSQL Database


Each layer has a specific responsibility.

---

# User Database Model

## Location


app/models/


The User model represents the users table in PostgreSQL.

The model defines:

- database columns;
- data types;
- relationships.

The User entity contains:


id

username

email

hashed_password

is_active

created_at

updated_at


---

# Why passwords are not stored directly

A major security requirement is:

Never store plaintext passwords.

Bad:


password = mypassword123


If the database is compromised, user passwords are exposed.

---

Instead, passwords are transformed using a hashing algorithm.

Registration flow:


Plain Password

    |

    v

Password Hashing

    |

    v

Stored Hash


The database stores:


$argon2id$...


rather than the original password.

---

# Schemas

## Location


app/schemas/


Schemas define the shape of data entering and leaving the API.

They are separate from database models.

---

# UserCreate Schema

Purpose:

Represents registration input.

Example:


{
username,
email,
password
}


This is what the API accepts from a new user.

---

# UserResponse Schema

Purpose:

Defines what information is returned to clients.

Sensitive information is excluded.

Example response:


{
id,
username,
email,
created_at
}


The hashed password is never returned.

---

# Why Models and Schemas are Separate

Models represent:


Database structure


Schemas represent:


API communication structure


They solve different problems.

A database user may contain:


hashed_password


but an API response should not expose that field.

---

# Repository Layer

## Location


app/repositories/users.py


The repository handles database operations related to users.

Examples:


create_user()

get_user_by_email()

get_user_by_username()

get_user_by_id()


---

# Why repositories exist

Without repositories:


Router

↓

Database Queries


would spread database logic throughout the application.

Repositories create a single place responsible for persistence.

---

# Service Layer

## Location


app/services/auth.py


The authentication service contains authentication business logic.

---

# Registration Process

The registration service performs:

1. Check whether email already exists.
2. Check whether username already exists.
3. Hash the password.
4. Create the User model.
5. Save the user.

Flow:


Registration Request

    |

    v

Auth Service

    |

    +--> Check existing users

    |

    +--> Hash password

    |

    +--> Create User

    |

    v

Repository

    |

    v

Database


---

# API Layer

## Location


app/api/auth.py


The API layer exposes authentication endpoints.

Initial endpoints:


POST /auth/register

POST /auth/login


---

# Registration Endpoint

The registration endpoint is responsible for:

- receiving HTTP requests;
- validating input;
- calling authentication services;
- returning responses.

The router does not:

- directly access PostgreSQL;
- hash passwords;
- contain authentication rules.

---

# Testing Registration

The registration system was tested successfully.

Verified:

## Successful registration

A new user could create an account.

Response:


id

username

email

is_active

created_at

updated_at


---

## Duplicate email protection

Attempting to register with an existing email was rejected.

This confirmed that business rules were being enforced.

---

# Login Verification

After registration was completed, login functionality was implemented.

The login process:


Login Request

    |

    v

Find User By Email

    |

    v

Verify Password Hash

    |

    v

Return User


---

# Password Verification

The application does not compare:


password == database password


because the database does not contain the original password.

Instead:


Provided Password

    |

    v

Hash Verification

    |

    v

Stored Password Hash


---

# Authentication Service Responsibility

The authentication service answers:

"Are these credentials valid?"

It does not handle:

- HTTP responses;
- JWT creation;
- database queries directly.

Those responsibilities belong elsewhere.

---

# Login Testing

The login flow was tested with:

## Correct credentials

Result:

Successful authentication.

---

## Incorrect password

Result:

Authentication rejected.

---

## Unknown email

Result:

Authentication rejected.

---

# JWT Preparation

After successful login verification, the next requirement was:

How does the application remember an authenticated user?

HTTP requests are stateless.

Example:

Request 1:


POST /auth/login


The server verifies identity.

Request 2:


POST /predict


The server does not automatically know who made the request.

---

# Solution

JWT authentication was introduced.

The future flow:


Login

↓

Verify credentials

↓

Create JWT

↓

Return token

↓

Client sends token with future requests

↓

Backend identifies user


---

# Current Authentication Status

Completed:

✅ User model  
✅ User schemas  
✅ User repository  
✅ Registration service  
✅ Registration endpoint  
✅ Password hashing  
✅ Duplicate user validation  
✅ Login verification  
✅ JWT token generation foundation  

Current unfinished milestone:

JWT validation and protected routes.

Next step:

Implement:


Depends(get_current_user)


to protect user-specific endpoints.

---

# Lessons Learned

## Authentication is a system, not a single endpoint

A secure authentication system requires:

- user storage;
- password protection;
- credential verification;
- identity persistence.

---

## Separation of responsibilities improves maintainability

Authentication logic is distributed intentionally:

Router:

HTTP communication.

Service:

Business rules.

Repository:

Database access.

Core:

Security utilities.

---

## Security decisions should be deliberate

Password handling and authentication mechanisms should never be treated as simple implementation details.