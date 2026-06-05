## Pull Request Template

### Description
<!-- Briefly describe what this PR does and why -->

### Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD improvement
- [ ] Maintenance task

### Checklist

#### Code Quality
- [ ] Tests added/updated and passing (`flutter test` / `pytest`)
- [ ] Code follows the project's style guidelines (check locally with `ruff check .` / `flutter analyze`)
- [ ] No new linting errors introduced
- [ ] Coverage maintained or improved

#### Documentation
- [ ] New features documented in relevant docs/ folder
- [ ] API changes reflected in `docs/api/` (if applicable)
- [ ] `SPEC.md` updated if the change affects the specification

#### Breaking Changes
- [ ] Migration scripts created (for database changes)
- [ ] Migration tested locally
- [ ] Changelog entry added (if applicable)

#### Testing
- [ ] Unit tests pass locally
- [ ] Backend: tests pass with `python manage.py test`
- [ ] Frontend: tests pass with `flutter test`

### Screenshots / Demo
<!-- Add screenshots or screen recordings for UI changes -->

### Related Issues
<!-- Link to related issues with: Fixes #123, Related to #456 -->

### Additional Notes
<!-- Any additional context reviewers should know -->

---

**Reminder**: All CI checks must pass before merging. The `main` branch is protected — direct pushes are not allowed.