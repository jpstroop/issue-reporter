# GitHub Reporter

A [Google Cloud Function](https://cloud.google.com/functions/) for reporting GitHub activity on a regular basis

## Dependencies

Function Dependencies are managed in `requirements.txt` because [that's what Google wants](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python). [`Pipfile`](https://github.com/pypa/pipfile) is used for development/debugging. Generally, you can just worry about tracking dependencies in `requirements.txt`, and calling `pipenv install -r requirements.txt` to update and keep things in sync. However, if you need to remove a dependency, it must be manually removed from both `requirements.txt` and `Pipfile`.

## Secrets

If a `secrets.json` file exists in the same directory as `main.py`, the required keys will be read from it. Otherwise, the function will look for the following environment variables, [which must be set when the function is deployed](https://cloud.google.com/functions/docs/env-var).
