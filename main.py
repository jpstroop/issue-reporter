from github_reporter import timestamp
from github_reporter.app_setup import load_config, load_secrets
from github_reporter.github_reporter import GithubReporter
from sys import stderr


def main(event={}, context={}):
    try:
        is_google_run = event.get("is_google_run", True)
        dump_to_stdout = event.get("dump_to_stdout", False)
        secrets = load_secrets()
        config = load_config()
        if is_google_run:
            print(f"{timestamp()} - Google called me")
        if dump_to_stdout:
            print(f"{timestamp()} - Local run, will dump JSON to stdout")
        gh_reporter = GithubReporter(secrets, config, dump_to_stdout)
        commit_success = gh_reporter.run_report()
        print(f"{timestamp()} - Commit success: {commit_success}")
        return True  # Cloud Functions must return something
    except Exception as e:
        print(f"{timestamp()} - {e}", file=stderr)
        return False


if __name__ == "__main__":
    main(event={"is_google_run": False, "dump_to_stdout": True})
