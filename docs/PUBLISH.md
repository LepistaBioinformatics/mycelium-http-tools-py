# Publish the package

## Prerequisites

- [poetry](https://python-poetry.org/docs/#installation)

## Steps

1. Build the package

```bash
poetry build --format wheel
```

2. Configure poetry to use the token

```bash
poetry config pypi-token.pypi <token>
```

3. Upload the package to the repository

```bash
poetry publish
```
