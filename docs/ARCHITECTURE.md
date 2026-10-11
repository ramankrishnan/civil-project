# NirmanConnect – System Architecture

## Overview

Three-tier application: React frontend, Flask REST API, PostgreSQL.

## User Roles
- Customer: browse, search, inquire, save
- Professional: profile, portfolio, respond to inquiries  
- Admin: moderate, verify, manage categories

## Azure Target
- Frontend: Azure Static Web Apps / Container Apps
- Backend: Azure Container Apps
- DB: Azure Database for PostgreSQL
- Storage: Azure Blob Storage
- Secrets: Azure Key Vault
