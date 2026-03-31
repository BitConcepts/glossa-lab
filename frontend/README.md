# Frontend

This directory contains the React frontend UI for Glossa Lab.

The frontend is the **primary user interaction layer**. It presents application state, workflows, configuration, and results to the user, but it does not own core runtime logic or service lifecycle. Those responsibilities belong to the backend.

## Responsibilities

- local application UI
- configuration and settings screens
- workflow and job management views
- service status and health views
- result inspection and visualization
- interaction with backend APIs
- user-triggered actions routed to backend interfaces

## Expected characteristics

- React-based
- cross-platform-friendly
- usable in local development and installed modes
- connected to explicit backend interfaces
- service-aware, but not service-owning
- clear separation between presentation and application logic

## Design rules

- core application logic does **not** live here
- service lifecycle management does **not** live here
- the frontend must not assume direct ownership of backend processes
- the frontend communicates with the backend only through explicit local APIs or documented interfaces
- UI state should remain distinct from backend runtime state

## Planned structure

Planned future additions include:

- frontend project configuration
- React application scaffold
- routing and layout structure
- API client layer
- configuration views
- workflow/job views
- results and inspection views
- status/health views
- tests

## Development expectations

The frontend should support at least two modes:

### Development mode
- runs through a local development server
- connects to a local backend endpoint
- supports rapid iteration without installed services

### Installed mode
- connects to a stable local backend endpoint
- behaves as a local application UI
- works cleanly with tray and background-service workflows

## Near-term implementation targets

1. React project scaffold
2. application shell and layout
3. backend API client layer
4. status and health view
5. configuration screens
6. workflow/job management views
7. result inspection views
