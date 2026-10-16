# Contributing

Members of the BSS video studio maintain this project. Anyone can report a bug or suggest an
improvement in the [issue tracker](https://github.com/BSStudio/bss-web-file-api/issues).

## Reporting a vulnerability

Don't open a public issue. Report it privately through
[GitHub private vulnerability reporting](https://github.com/BSStudio/bss-web-file-api/security/advisories/new).
The [security policy](https://github.com/BSStudio/bss-web-file-api/security/policy) explains what happens next.

## Pull requests

Open a pull request against `main`. A change is accepted when:

- The title follows [Conventional Commits](https://www.conventionalcommits.org/). Releases and
  release notes are generated from it.
- `isort`, `black`, `mypy` and `pylint` pass. See [Lint](README.md#lint).
- New or changed behaviour comes with tests, and unit-test coverage stays at 100%
  (`uv run pytest tests --cov=src --cov-fail-under=100`).
- The integration tests pass. See [Integration Test](README.md#integration-test).

Pull requests are squash-merged through the merge queue once the required checks pass.
