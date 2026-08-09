# CyberSafe

> Protect Yourself Before It's Too Late.

CyberSafe is a cybersecurity awareness and protection platform designed to helo student, individuals, families, and small organizations better understand, detect, and respond to common digital threats.

The platform combiens security analysis tools, educational content, simulations, personalized recommendations, and security monotoring into a single environment.


---

## Objectives

CyberSafe aims to make cybersecurity more accessible and actionable by allowing users to :

- Anamlyze potentially dangerous URLS.
- Evaluate password strength.
- Generate stronger passwords;
- Check for sign of email or account compromise.
- Scan suspicions files.
- Learn how to recognize phishing and scams.
- Receive personalized security recommandations.
- Follow threir security activity security alerts.

---

## Main Features

### Security Analysis

- URL and website analysis
- Password analysis and generation
- Email compromise cheking
- File security analysis
- Security scoring

### Awareness and Learning

- Cybersecurity guides
- Anti-scam educational content 
- Quizzes
- Phishing simulations
- Security recommendations

### Monitoring and Alerts

- Security alerts
- User activity history
- Security statistics
- Personalized notifications

### Administration

- User management
- Security content management
- Platform monotoring
- Administrative dashboard

---


## Architecture

CyberSafe is designed as a modular platform composed of several major domains:

1. Identity 
2. Asset Management
3. Analysis
4. Decision Engine
5. Learning
6. Notification
7. Administration
8. Monotoring

These domains are developd progressively through dedicated architecture sprints.

---

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

### Backend

- Python
- FastAPI

### Database

- PostgreSQL

### Cache and Messaging

- Redis

### Infrastructure

- Docker
- Docker Compose
- Nginx

### Dvelopment

- Git
- GitHub
- VS Code
- WSL2
- Ubuntu

---


## Project Structure

```text
cybersafe-platform
|
|- apps/
    |- web/
    |- api/
    |- admin/

|- packages/
    |- ui/
    |- types/
    |- config/
    |- shared/

|- infractruture/
    |- docker/
    |- nginx/
    | scripts/

|- docs/
    |- architecture/
    |- database/
    |- api/
    |- journal/

|- .github/
    |- workflows/

|- docker-compose.yml
|- pnpm-workspace.yml
|- README.md
|- .gitignore
|- LICENSE


```

The structure will evolve as the project progresses.


## Security Principles

Security is a core requirement of CyberSafe;

The project follows principles including:

- Secure-by-design development
- Least privilege
- Defense in depth
- Input validation
- Secure authentication
- Secure secret management
- Data minimization
- Auditability
- Privacy by design
- Explicit authorization
- Safe handling of security analysis results

Security-sensitive features will be implemented in controlled and ethical ways.


## Project Status

CyberSafe is currently under active development.

The architecture and technical foundations are being progressively implemented.

Architecture Sprints

 Sprint Architecture 1 — Identity
 Sprint Architecture 2 — Asset Management
 Sprint Architecture 3 — Analysis
 Sprint Architecture 4 — Decision Engine
 Sprint Architecture 5 — Learning
 Sprint Architecture 6 — Notification
 Sprint Architecture 7 — Administration
 Sprint Architecture 8 — Monitoring

## Development Environment

The current development environment is based on:

- Windows 11
- WSL2
- Ubuntu
- Docker Desktop
- Git
- Node.js
- Python
- pnpm


## Documentation

Project documentation will be progressively added under:

docs/

including:

- Architecture documentation
- Database design
- API documentation
- Security decisions
- Development journal

## Disclaimer

CyberSafe is designed for defensive cybersecurity education, awareness, analysis, and protection.

Security testing and simulation features must only be used against systems, accounts, files, URLs, and environments for which the user has appropriate authorization.


## License

License information will be added before the first public release.


## Author

WILFREDSOH

Cybersecurity and Software Development Student


## Vision

CyberSafe aims to become a practical cybersecurity companion that helps users understand digital risks before those risks become real incidents.

### Protect Yourself Before It's Too Late.

---


