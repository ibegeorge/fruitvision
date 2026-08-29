# Development Log 004: JWT Authentication

## Objective

Implement secure authentication for FruitVision using JSON Web Tokens (JWT).

Before JWT implementation, FruitVision could:

- register users;
- securely store passwords;
- verify login credentials.

However, the application had no mechanism to remember an authenticated user across multiple requests.

The purpose of JWT authentication was to allow users to authenticate once and securely access protected resources afterward.

---

# The Problem JWT Solves

HTTP requests are stateless.

This means that after a user successfully logs in:

```
POST /auth/login
```

the next request:

```
GET /users/me
```

does not automatically know who made the request.

The backend needs a secure way to identify the user making each request.

---

# JWT Solution

JWT provides a signed token that represents the identity of an authenticated user.

The authentication flow becomes:

```
User Login

        |
        v

Verify credentials

        |
        v

Generate JWT

        |
        v

Return token to client

        |
        v

Client sends token with future requests

        |
        v

Backend validates token

        |
        v

Identify authenticated user
```

---

# JWT Structure

A JWT consists of three parts:

```
HEADER.PAYLOAD.SIGNATURE
```

---

## Header

The header contains information about the token type and signing algorithm.

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

---

## Payload

The payload contains claims about the user.

FruitVision uses:

```json
{
  "sub": "1",
  "exp": "expiration_time"
}
```

---

## Subject (`sub`) Claim

The `sub` claim identifies the owner of the token.

In FruitVision:

```
sub = user_id
```

Example:

```json
{
    "sub": "1"
}
```

means:

The token belongs to the user with ID 1.

---

## Expiration (`exp`) Claim

JWT tokens are temporary.

The expiration claim determines when the token becomes invalid.

Example:

```
Token created:

10:00 AM


Expiration:

10:30 AM
```

After expiration, the backend rejects the token.

---

# JWT Configuration

JWT configuration was moved into application settings rather than being hardcoded.

The configuration flow:

```
.env

↓

Settings

↓

Security Module

↓

JWT Operations
```

Environment variables include:

```
JWT_SECRET_KEY

JWT_ALGORITHM

JWT_ACCESS_TOKEN_EXPIRE_MINUTES
```

---

# Security Module

Location:

```
app/core/security.py
```

The security module is responsible for authentication-related cryptographic operations.

Responsibilities:

- password hashing;
- password verification;
- JWT creation;
- JWT decoding.

Keeping security logic centralized prevents duplication across the application.

---

# JWT Creation

The function:

```python
create_access_token()
```

was implemented.

Its responsibility:

Convert user identity information into a signed JWT.

Example:

Input:

```python
{
    "sub": "1"
}
```

Output:

```
eyJhbGciOiJIUzI1Ni...
```

The token is then returned during login.

---

# JWT Decoding

The reverse operation was implemented through:

```python
decode_access_token()
```

Its responsibility:

Take a JWT string and verify:

- the signature;
- the algorithm;
- the expiration.

Example:

Input:

```
eyJhbGciOiJIUzI1...
```

Output:

```python
{
    "sub": "1",
    "exp": 178....
}
```

---

# OAuth2 Integration

FastAPI's:

```python
OAuth2PasswordBearer
```

was introduced to connect JWT authentication with FastAPI's security system and Swagger documentation.

The dependency extracts the JWT token from:

```
Authorization: Bearer <token>
```

Example:

```
Authorization: Bearer eyJhbGciOi...
```

---

# FastAPI Dependency Injection

A major concept introduced during JWT implementation was dependency injection.

The purpose was to avoid repeating authentication logic in every protected endpoint.

Without dependencies:

```
/users/me

decode token

find user


/predictions

decode token

find user


/history

decode token

find user
```

This creates duplication.

---

Using FastAPI dependencies:

```python
Depends(get_current_user)
```

authentication logic is centralized.

The flow becomes:

```
Request

↓

Dependency executes

↓

Validate JWT

↓

Find user

↓

Endpoint receives user
```

---

# Current User Dependency

Location:

```
app/api/dependencies.py
```

The function:

```python
get_current_user()
```

was created.

Its responsibilities:

1. Receive JWT token.
2. Decode token.
3. Extract user ID.
4. Retrieve user from database.
5. Confirm user exists.
6. Return authenticated User object.

Flow:

```
JWT Token

↓

Decode token

↓

Extract user_id

↓

Query database

↓

Return User
```

---

# Protected Route Implementation

A protected endpoint was created:

```
GET /users/me
```

This endpoint returns information about the currently authenticated user.

The route uses:

```python
Depends(get_current_user)
```

which ensures that only authenticated users can access it.

---

# Authentication Lifecycle

The completed authentication flow:

```
User Registration

        |
        v

Password Stored Securely

        |
        v

User Login

        |
        v

Credentials Verified

        |
        v

JWT Generated

        |
        v

JWT Returned To Client

        |
        v

Authorization Header Sent

        |
        v

JWT Validated

        |
        v

Current User Retrieved
```

---

# Swagger Authentication Flow

Swagger was configured to work with the JWT authentication system.

The process:

1. User opens Swagger documentation.
2. User selects Authorize.
3. User provides login credentials.
4. Swagger sends credentials to:

```
POST /auth/login
```

5. Backend validates credentials.
6. Backend returns JWT.
7. Swagger stores the token.
8. Swagger attaches:

```
Authorization: Bearer <token>
```

to protected requests.

---

# API Response Protection

During implementation, the `/users/me` endpoint initially returned the SQLAlchemy User model directly.

This exposed internal database fields.

Example:

```json
{
    "id": 1,
    "email": "user@example.com",
    "hashed_password": "$argon2id..."
}
```

This is unsafe.

The solution was to use a response schema:

```
Database Model

        |

        v

Response Schema

        |

        v

API Response
```

The `UserResponse` schema controls what information leaves the backend.

Sensitive fields such as:

```
hashed_password
```

are excluded.

---

# Files Created or Modified

## Security

```
app/core/security.py
```

Added:

- JWT decoding functionality.

---

## Dependencies

```
app/api/dependencies.py
```

Added:

- OAuth2 token extraction.
- Current user resolution.

---

## Authentication Router

```
app/api/auth.py
```

Updated:

- Login endpoint to support OAuth2 authentication flow.

---

## Users Router

```
app/api/users.py
```

Added:

- Protected `/users/me` endpoint.
- Response schema filtering.

---

# Testing Performed

Manual verification was completed.

Verified:

✅ User registration works.

✅ Duplicate users are rejected.

✅ Login credentials are validated.

✅ JWT tokens are generated.

✅ Swagger authorization works.

✅ Protected routes reject unauthenticated requests.

✅ Authenticated users can access `/users/me`.

✅ Sensitive fields are not exposed in API responses.

---

# Key Lessons Learned

## Authentication is a system, not a single endpoint

A secure authentication system requires:

- identity creation;
- password protection;
- credential verification;
- token generation;
- token validation;
- protected resources.

---

## Authentication and authorization are different

Authentication answers:

> "Who are you?"

Authorization answers:

> "What are you allowed to access?"

JWT primarily helps establish identity.

---

## Database models should not be exposed directly

Database structures and API responses serve different purposes.

Models represent internal persistence.

Schemas represent external communication.

---

## Dependency Injection Improves Maintainability

FastAPI dependencies allow reusable logic such as authentication checks to be written once and used throughout the application.

---

# Milestone Status

Completed:

✅ JWT configuration  
✅ JWT token generation  
✅ JWT token decoding  
✅ OAuth2 integration  
✅ Swagger authentication flow  
✅ FastAPI dependency injection  
✅ Current user resolution  
✅ Protected user endpoint  
✅ Response data filtering  

---

# Next Milestone

The authentication foundation is complete.

The next phase of FruitVision development is the Prediction System.

The upcoming workflow:

```
Authenticated User

        |
        v

Upload Fruit Image

        |
        v

Store Image

        |
        v

Run Machine Learning Model

        |
        v

Generate Prediction

        |
        v

Store Prediction History
```

This will introduce:

- file uploads;
- new database relationships;
- prediction models;
- AI inference integration.