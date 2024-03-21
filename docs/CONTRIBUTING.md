# Contributing to Hotmart-Python

First off, thank you for considering contributing to Hotmart-Python. It's people like you that make
Hotmart-Python such a great tool.

## Quick start

1. Fork the hotmart-python repo.

```bash
git clone https://github.com/im-voracity/hotmart-python.git
```

2. Create a virtual environment and install the dependencies. (We
   use [Poetry](https://python-poetry.org/))

```bash
poetry install
```

and you're good to go!

## Where do I go from here?

If you've noticed a bug or have a feature request, make one!

## Fork & create a branch

If this is something you think you can fix, then fork Hotmart-Python and create a branch with a
descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```bash
git checkout -b 325-add-japanese-translations
```

Go to the GitHub page of this fork. You can now send your pull request! Make sure to target the
project's master branch.

## Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and
that you need to update your branch, so it's easier to merge. To learn more about rebasing in Git,
there are a lot of [good resources](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) but
here's the suggested workflow:

```bash
git checkout add-japanese-translations
git pull --rebase upstream master
git push --force-with-lease add-japanese-translations
```

## Merging a PR (maintainers only)

A PR can only be merged into master by a maintainer if:

- It's test are passing.
- It has been approved by a maintainer.
- It has no requested changes.
- It is up to date with the target branch.

Any maintainer is allowed to merge a PR if all of these conditions are met.
