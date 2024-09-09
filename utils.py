def read_env_file(file_path):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars


def get_response(url):
  import requests

  env_vars = read_env_file('.env')
  cookie = env_vars['HACKERRANK_COOKIE']

  if not cookie:
    raise ValueError("HACKERRANK_COOKIE is not set.")
    
  headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-encoding': 'gzip, deflate, br, zstd',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'cache-control': 'no-cache',
      'cookie': cookie,
      'dnt': '1',
      'pragma': 'no-cache',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
  }

  response = requests.get(url, headers=headers)
  data = response.json()

  return data


def get_submissions(contest_slug, limit=1000):
  url = f"https://www.hackerrank.com/rest/contests/{contest_slug}/judge_submissions/?offset=0&limit={limit}&_=1724666352377"
  response = get_response(url)
  return response['models']


def download_submissions(submissions, retry_count=-1):
    import sys

    failed_submissions = []
    retry_count = retry_count if retry_count >= 0 else len(submissions)

    import os
    if not os.path.exists('submissions'):
        os.makedirs('submissions')
    
    for i, submission in enumerate(submissions):
        try:
            code = get_response(url=f"https://www.hackerrank.com/rest/contests/reidxtreme3-initial-round/submissions/{submission['id']}")
            print(code)
            code = code['model']['code']
            with open(f"submissions/{submission['id']}.txt", 'w') as file:
                file.write(code)
        except Exception as e:
            failed_submissions.append(submission)
        sys.stdout.write(f"\rProgress: {i+1}/{len(submissions)} \t Failed: {len(failed_submissions)}")
        sys.stdout.flush()

        retry_count -= 1

    if len(failed_submissions) > 0:
        print(f"Failed to download {len(failed_submissions)} submissions: {failed_submissions}")
        if retry_count > 0:
            print(f"Retrying {retry_count} more times...")
            download_submissions(failed_submissions, retry_count)
        else:
            print("Failed to download all submissions.")

def get_submission_data(submission_id, submissions):
    return next((submission for submission in submissions if submission['id'] == submission_id), None)