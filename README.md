# Filename validation
Pre-commit hook for validating Python filenames.

*Note: This hook was created for my article [How to Create a Pre-Commit Hook](https://stefaniemolin.com/articles/devx/pre-commit/hook-creation-guide/).*

## Usage

Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/stefmolin/filename-validation
  rev: 0.1.0
  hooks:
    - id: validate-filename
```

The `validate-filename` hook supports custom minimum lengths with the `--min-len` command line argument:

```yaml
- repo: https://github.com/stefmolin/filename-validation
  rev: 0.1.0
  hooks:
    - id: validate-filename
      args: [--min-len=5]
```

Be sure to check out the [pre-commit documentation](https://pre-commit.com/#pre-commit-configyaml---hooks) for additional configuration options.
