
# Developer Instructions:

- Run all linters: `inv lint`
- Run one specific linter: `inv lint --linter=<linter_name>`, where linter name is one of:
  - terraform
  - javascript
  - black
  - isort
  - jscpd
  - flake8
  - pylint
  - mypy
  - bash
  - hadolint
- Run automatic fix of lint improvements: `black . && isort .`