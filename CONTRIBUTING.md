# Contributing

Thanks for your interest in the Yggdrasil AI Labs feeder family.

## Ground rules

- Open an issue before large changes so we can align on scope.
- Every repo runs a gated pipeline: **pytest + coverage → SonarCloud quality gate → Snyk SCA → build**. PRs must keep it green.
- Match the existing style; keep changes focused and single-purpose — no drive-by reformatting.

## Local checks

    pip install -r requirements-dev.txt
    pytest --cov

## Pull requests

Target `main`, describe what changed and why, and link any related issue.
