# API Reference

Base: http://localhost:5000/api

## Auth
POST /auth/register  POST /auth/login  GET /auth/me

## Professionals  
GET /professionals  GET /professionals/:id  PUT /professionals/me

## Inquiries
POST /inquiries  GET /inquiries  PATCH /inquiries/:id/status

## Admin
GET /admin/dashboard  POST /admin/professionals/:id/verify
