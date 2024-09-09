Since the hackerrank platform seems to be buggy and does not have some features, had to write custom scripts to get some things done in a recent contest we held. (ReidExtreme 3.0)

These scripts calls the hackerrank REST api using the cookie extracted from the browser.

# Scripts

- plagiarism - Downloads all submissions and cross check them for plagiarims. (Hackerrank does not have a built in checker)
- leaderboard - Get all submission data and creates a leaderboard. (At the time of writing there is a bug that causes partial marks to not appear in the leaderboard)

# Usage

- Create a .env file with the same format as .env.sample
- Get the cookie header from hakerrank api reqiests. (Network tab in chrome dev tools)
- set the cookie in .env
- run a sample

# Extending

Util functions have docstrings and main scripts aren't that complex. To add a functianality, find the endpoint to get relevent data and use the `get_response` from `utils`.

Good Luck!