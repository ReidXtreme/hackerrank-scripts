import utils
import difflib
import sys

def compare_submissions(submissions):
    similarities = {}
    total_pairs = len(submissions) * (len(submissions) - 1) // 2
    processed_pairs = 0
    for i, submission1 in enumerate(submissions):
        for j, submission2 in enumerate(submissions):
            if i < j:  # Ensure each pair is only compared once
                processed_pairs += 1
                sys.stdout.write(f"\rProgress: {processed_pairs}/{total_pairs}")
                sys.stdout.flush()
                
                if submission1['challenge_id'] != submission2['challenge_id']:
                    continue
                if submission1['hacker_id'] == submission2['hacker_id']:
                    continue
                
                with open(f"submissions/{submission1['id']}.txt", 'r') as file1:
                    code1 = file1.read()
                with open(f"submissions/{submission2['id']}.txt", 'r') as file2:
                    code2 = file2.read()
                    
                similarity = difflib.SequenceMatcher(None, code1, code2).ratio()
                similarities[(submission1['id'], submission2['id'])] = similarity
    sys.stdout.write("\n")
    return similarities

# download submissions
submissions = utils.get_submissions('sample-contest')
utils.download_submissions(submissions, -1)


similarities = compare_submissions(submissions)

similarity_list = []

for pair, similarity in similarities.items():
    similarity_list.append((pair, similarity))

similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

# Example to print the similarities
for pair, similarity in similarity_list:
    if similarity > 0.9:  # Filter out similarities above a certain threshold
        
        submission1_data = utils.get_submission_data(pair[0], submissions)
        submission2_data = utils.get_submission_data(pair[1], submissions)

        if submission1_data['challenge']['name'] == 'Battleships 3':
            continue
        print(f"Submissions {pair[0]} and {pair[1]} have a similarity of {similarity}")
        if submission1_data:
            print(f"Challenge: {submission1_data['challenge']['name']}, Hacker: {submission1_data['hacker_username']}")
        else:
            print(f"No data found for submission {pair[0]}")
        if submission2_data:
            print(f"Challenge: {submission2_data['challenge']['name']}, Hacker: {submission2_data['hacker_username']}")
        else:
            print(f"No data found for submission {pair[1]}")
        print("\n")
