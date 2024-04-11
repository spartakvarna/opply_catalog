# AWS Migration Plan

## Overview
This README outlines the migration of our SQL database to Amazon RDS and the adoption of AWS Cognito for enhanced user management and access control, based on successful strategies implemented for puzzlecv.com.
The approach is the same as for puzzlecv.com. We can go through it if necessary.

## Migration to Amazon RDS
- Export SQL database and import it into a new RDS instance.
- Update application configurations to point to RDS.

## User Management with AWS Cognito
- Setup AWS Cognito for handling user registrations, logins, and role-based access control.
- Integrate Cognito into the application to manage user authentication and authorization.

## Access Control
- **Admin Users**: Exclusive access to Product CRUD endpoints.
- **Customers**: Can create orders and view their order history. Access to others' order data is restricted.

## Business Logic
- **Goes to AWS Lambda**
