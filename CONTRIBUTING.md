# contributing to CyberSafe

Thank you fro your interest in CyberSafe.

## Development Principles

CyberSafe follows these principles :

- Security ny design
- Clean and maintainable code
- Explicit documentation
- Small and focused changes
- Automated testing 
- Code review before merging
- No secrets committed to Git 
- Defensive and ethical cybersecurity practices

## Git Workflow

The main branch is :


main

New fratures should be developed in dedicated branches.

Example : 
feature/url-analysis
feature/password-analysis
feature/user-authentication
fix/login-validation

Commit Convention

Commits should be clear and descriptive.

Examples:

feat: add URL analysis service
fix: validate password input
docs: update architecture documentation
test: add URL analyzer tests
refactor: simplify analysis service
chore: update dependencies

Security

Never commit : 
- passwords
- API keys
- private keys
- tokens
- production credentials
- personal secret
- real user data

Use environment varaibles for sensible configuration.

Pull Requests

Before merging a change:
 1. Verify the application builds.
 2. Run tests.
 3. Run linting
 4. Check type safety.
 5. Review security implications.
 6. Update documentation when necessary.


 	
