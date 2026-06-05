# Contributing to Home Ops Hub

Thank you for contributing! This document explains our workflow, standards, and how to get your changes merged.

---

## Quick Start

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/YOUR_USERNAME/home-ops-hub.git
cd home-ops-hub

# 2. Set up pre-commit (required before first commit)
pip install pre-commit
pre-commit install

# 3. Create a feature branch
git checkout -b feat/your-feature-name

# 4. Make changes, commit, push
git add .
git commit -m "feat(scope): add awesome new feature"
git push origin feat/your-feature-name

# 5. Open a Pull Request
```

---

## Branch Strategy

| Branch | Purpose | Protected? |
|--------|---------|------------|
| `main` | Production-ready code | ✅ Yes |
| `develop` | Integration branch for next release | ✅ Yes |
| `feat/*` | Feature development | No |
| `fix/*` | Bug fixes | No |
| `chore/*` | Maintenance, refactoring | No |

**Rules:**
- Never push directly to `main` or `develop`
- Feature branches are created from `develop`
- PRs must pass all CI checks and get at least 1 review

---

## Commit Message Format

We follow **Conventional Commits** (`type(scope): description`):

```
feat(assets): add QR code generation for devices
fix(dashboard): correct warranty expiry date calculation
docs(api): update asset endpoint documentation
ci(workflows): add Docker security scanning
chore(deps): update Django to 5.1.1
refactor(models): extract shared validation logic
test(consumables): add unit tests for stock alerts
```

**Types:**
| Type | Description |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no feature change |
| `test` | Adding or updating tests |
| `ci` | CI/CD changes |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |

**Rules:**
- Use imperative mood ("add" not "added")
- Keep subject line under 72 characters
- Reference issues: `Closes #123` or `Related to #456`

---

## Code Standards

### Python (Backend)
```bash
# Lint & format
cd backend
ruff check .
ruff format .

# Run tests
python manage.py test

# Full check before PR
python manage.py check
ruff check .
pytest --cov=apps --cov-report=term-missing
```

### Flutter / Dart (Frontend)
```bash
# Analyze & format
cd frontend
flutter analyze
flutter format .

# Run tests
flutter test

# Check dependencies
flutter pub outdated
```

---

## Pre-commit Hooks

Installed automatically via `pre-commit install`. They run on every `git commit`:

1. **Trailing whitespace** — remove trailing spaces
2. **End-of-file fixer** — ensure files end with newline
3. **YAML/JSON validation** — catch syntax errors
4. **Large files** — prevent committing files > 5MB
5. **Merge conflict markers** — block accidental conflicts
6. **Conventional commit** — validate commit message format
7. **Ruff** — Python lint & format (backend)
8. **Flutter analyze** — Dart lint (frontend)

To skip hooks temporarily (rare): `git commit --no-verify -m "..."`

---

## Pull Request Checklist

Before requesting review, verify:

- [ ] All CI checks pass (GitHub Actions green)
- [ ] New tests added and passing
- [ ] `flutter analyze` / `ruff check` pass with no new issues
- [ ] `SPEC.md` updated if feature changes the spec
- [ ] No debug code or TODOs left behind
- [ ] PR description filled out (use the template)
- [ ] Related issues linked

---

## Testing Standards

| Layer | Tool | Requirement |
|-------|------|------------|
| Python | pytest | Coverage >= 80% for new code |
| Dart | flutter test | All new features tested |
| API | DRF APIClient | Endpoint tests for all endpoints |
| Integration | Django test client | Form submissions, auth flows |

Run all tests locally before pushing:
```bash
# Backend
cd backend && pytest --cov=apps -q

# Frontend
cd frontend && flutter test
```

---

## Setting Up Local Environment

```bash
# Docker (PostgreSQL + Redis + MinIO)
cd infrastructure
docker compose up -d

# Backend
cd backend
cp .env.example .env  # Edit with your settings
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
flutter pub get
flutter run
```

---

## Code Review Guidelines

Reviewers will check:
- **Correctness** — does it do what it says?
- **Maintainability** — will others understand this in 6 months?
- **Testing** — are edge cases covered?
- **Performance** — any N+1 queries, unnecessary rebuilds?
- **Security** — no sensitive data exposed, proper auth checks

Be respectful and constructive. Every suggestion should explain *why*.

---

## Questions?

Open a discussion or ping in any PR. We're happy to help!