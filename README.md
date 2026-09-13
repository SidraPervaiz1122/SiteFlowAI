# SiteFlow AI — Construction Workflow & IPC Management

SiteFlow AI is an AI-powered construction project-control platform for residential and commercial works. Built for deterministic quality assurance and financial control, it digitizes the complete lifecycle from Check Requests to Interim Payment Certificates (IPC).

[![Build Status](https://github.com/SidraPervaiz1122/SiteFlowAI/actions/workflows/ci.yml/badge.svg)](https://github.com/SidraPervaiz1122/SiteFlowAI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Documentation

Full project documentation has been organized into the `docs/` directory:

- [**Architecture & Workflow**](docs/architecture.md) — Backend/Frontend tech stack, RBAC, database schema, and the AI layer.
- [**Getting Started**](docs/getting-started.md) — Local development setup, demo credentials, and running tests.
- [**API Reference**](docs/api-reference.md) — Summary of main FastAPI routes.
- [**Deployment Guide**](docs/deployment.md) — Azure App Service CI/CD pipeline and required secrets.
- [**Troubleshooting**](docs/troubleshooting.md) — Common deployment issues and their fixes.

## Project Structure

```text
.
├── backend/          # FastAPI backend application
├── frontend/         # React SPA (Vite + TS)
├── scripts/          # Utility scripts
└── docs/             # Project documentation
```

## Contributing

To contribute to SiteFlow AI:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
