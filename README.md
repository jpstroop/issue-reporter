# GitHub Reporter

A [Google Cloud Function](https://cloud.google.com/functions/) for reporting GitHub activity on a regular basis

## Dependencies

Function Dependencies are managed in `requirements.txt` because [that's what Google wants](https://cloud.google.com/functions/docs/writing/specifying-dependencies-python). [`pipenv`](https://github.com/pypa/pipenv) is used for development/debugging. Generally, you can just worry about tracking dependencies in `requirements.txt`, and calling `pipenv install -r requirements.txt` to update and keep things in sync. However, if you need to remove a dependency, it must be manually removed from both `requirements.txt` and `Pipfile`.

## Secrets

If a `secrets.json` file exists in the same directory as `main.py`, the required keys will be read from it. Otherwise, the application will look for the following environment variables, [which must be set when the function is deployed](https://cloud.google.com/functions/docs/env-var). The following must be set:

 * `GITHUB_TOKEN` (See https://github.com/settings/tokens)
 * `GITHUB_ORGANIZATION`

Sample `secrets.json`:

```json
{
  "GITHUB_TOKEN":"1a2b3c4d5e6f7g8h9i0k",
  "GITHUB_ORGANIZATION":"my_org"
}
```

## Caching

[`PyGithub`](https://github.com/PyGithub/PyGithub) doesn't do a great job of memoizing API responses (i.e. it makes several repetitive calls), so [`requests-cache`](https://github.com/reclosedev/requests-cache) is used to speed things up and help keep us from hitting the GitHub API request limit. API responses are cached locally for 5 minutes in memory. This should all happen perfectly transparently. Just letting you know.

## Time Range

Issues changed over the past 24 hours are reported. This is presently hard-coded but could be made a configuration option (as an arg to a `timedelta`?) in the future.

## Related

https://gist.github.com/jpstroop/6ed0c98f6a960f69f8142b56064cdb84

## JSON Data

Reports are serialized as JSON data, with issues grouped using the repository name as the key. The structure is as follows:

```javascript
{
  "today": "2019-09-27T00:01:07",
  "yesterday": "2019-09-26T00:01:07",
  "repo_name": [
    {
      "created_at": "2019-09-25T17:51:05",
      "html_url": "https://github.com/my_org/repo_name/pull/42",
      "number": 42,
      "pull_request_html_url": "https://github.com/my_org/repo_name/pull/42",
      "repository_html_url": "https://github.com/my_org/repo_name",
      "state": "closed",
      "title": "The widget is broken",
      "user_name": null,
      "comments": [
        {
          "user_name": "Abe Developer",
          "updated_at": "2019-09-26T15:05:47",
          "html_url": "https://github.com/my_org/repo_name/pull/42#issuecomment-535137315",
          "body": "Fixes all the things (note that this could contain Markdown)"
        }
      ],
      "events": [
        {
          "actor_name": "Ann Actor",
          "created_at": "2019-09-26T17:42:41",
          "type": "merged"
        },
        {
          "actor_name": "Ann Actor",
          "created_at": "2019-09-26T17:42:41",
          "type": "closed"
        }
      ]
    },
    {
      "created_at": "2019-09-26T17:48:22",
      "html_url": "https://github.com/my_org/repo_name/issues/496",
      "number": 496,
      "pull_request_html_url": null,
      "repository_html_url": "https://github.com/my_org/repo_name",
      "state": "open",
      "title": "Fixes one more thin",
      "user_name": null,
      "comments": [],
      "events": []
    }
  ],
  "repo_name1": [
    {
      "created_at": "2019-09-26T15:31:16",
      // ...
    }
  ]
}
```
