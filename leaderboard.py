import utils

submissions = utils.get_submissions('sample_contest')

scores_by_team = {}

for submission in submissions:
  team = submission['hacker_username']
  challenge = submission['challenge']['slug']
  score = submission['score']
  time = submission['inserttime']

  if team not in scores_by_team:
    scores_by_team[team] = {}
  if challenge not in scores_by_team[team]:
    scores_by_team[team][challenge] = (0, 0)

  if score > scores_by_team[team][challenge][0]:
    scores_by_team[team][challenge] = (score, time)

print(scores_by_team)

total_scores_by_team = {}

for team, challenges in scores_by_team.items():
    total_score = sum(score for score, _ in challenges.values())
    total_time = sum(time for _, time in challenges.values())
    total_scores_by_team[team] = (total_score, total_time)


sorted_teams = sorted(total_scores_by_team.items(), key=lambda x: (-x[1][0], x[1][1]))
print(f"Rank\tTeam\tTotal Score")
for rank, (team, (total_score, _)) in enumerate(sorted_teams, 1):
    print(f"{rank}\t{team}\t{total_score:.2f}")

def print_scores_with_problem_names(team_name):
    if team_name in scores_by_team:
        print(f"Scores for {team_name}:")
        for challenge, (score, _) in scores_by_team[team_name].items():
            print(f"{challenge}: {score}")
    else:
        print(f"No scores found for {team_name}.")

for team in scores_by_team.keys():
    print_scores_with_problem_names(team)
    print("\n")