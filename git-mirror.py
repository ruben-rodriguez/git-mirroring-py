from __future__ import print_function
from builtins import input

import time
import json
import os
import requests
import signal
import subprocess
import sys

def signal_handler(signum, frame):
    """Signal handler that captures SIGINT and stops the application"""

    print("\t\n\nSignal", signal.Signals(signum).name, "received, exiting...\n")
    sys.exit(0) 

def check_git():
    """Checks if git is installed in the system"""

    print("\n\tChecking git version installed...")

    try:

        output = subprocess.check_output("git --version", shell=True, stderr=subprocess.STDOUT)
        print("\t", output.decode('ascii'))
        return True

    except subprocess.CalledProcessError as e:

        print("\n\tCould not find git command on the system...")
        print("\t", e)
        return False

def check_dir(path):
    """Checks if pointed path to store git repositories exists in the system"""

    print("\tChecking if ", path, "exists...")

    if(os.path.isdir(path)):

        print("\tDirectory '", path, "' exists")
        return True

    else:

        print("\tDirectory '", path, "' does not exist")
        return False
    
def get_number_of_repos(username):
    """Gets the number of repositories hosted on GitHub for the given username"""

    try:

        r = requests.get('https://api.github.com/users/ermus19', timeout=10)

    except requests.exceptions.RequestException as e:

        print("\n\tException raised during connection:")
        print("\t", e)
        print("\tCheck System's connectivity and try again, exiting...\n\n")
        sys.exit(1)

    if(r.status_code == 200):

        print("\tUser ", username,  " data successfully collected!")

        try:

            with open('user_data.json', 'w') as response_data:

                json.dump(r.json(), response_data, indent=4)
                data = json.dumps(r.json(), indent=4)

        except IOError as e:

            print("Could not open the file to store data:")
            print(e)
            sys.exit(0)

        user_list = json.loads(data)
        repos_len = user_list['public_repos']

        print("\tNumber of public repos found:", repos_len)

        return repos_len
      
    else: 

        print("Could not collect user information...")
        sys.exit(0)

def get_repos_url(username, repos_len):
    """Gets the URL of all the user's repositories hosted on GitHub"""

    try:

        r = requests.get('https://api.github.com/users/ermus19/repos')

    except requests.exceptions.RequestException as e:

        print("\n\tException raised during connection:")
        print("\t",e)
        print("\tCheck System's connectivity and try again\n\n")
        sys.exit(1)

    if (r.status_code == 200):

        print("\tGitHub API data successfully collected for user", username,  "!")

        try:

            with open('repos_data.json', 'w') as response_data:

                json.dump(r.json(), response_data, indent=4)
                data = json.dumps(r.json(), indent=4)

        except IOError:

            print("\t\nCould not open the file to store data...")
            sys.exit(0)

        repositories_dictionary = json.loads(data)
        urls = []

        print("\n\tList of repositories urls: \n")

        for index in range(0, repos_len):

            url = repositories_dictionary[index]['html_url']
            print("\t", url)
            urls.append(url)

        print("\n")
        return urls

    else:

        print("Could not connect to GitHub API server...")
        sys.exit(0)

def do_mirror(username, path):
    """Clones/pulls the remote repositories to the local path"""

    start_time = time.time()

    is_valid_dir = check_dir(path)

    if(is_valid_dir):

        repos_len = get_number_of_repos(username)

        if(repos_len > 0):

            repos_url = get_repos_url(username, repos_len)

            for repo in repos_url:

                repo_split = repo.split('/')
                repo_name = repo_split[len(repo_split) - 1]

                git_check = 'git -C ' + path + '/' + repo_name + ' rev-parse'
                git_clone = 'git -C ' + path + ' clone ' + repo
                git_pull = 'git -C ' + path + '/' + repo_name + ' pull --all'

                print("\tWorking on " + repo_name + " repository...")

                try:

                    output = subprocess.check_output(git_check, shell=True, stderr=subprocess.STDOUT)
                    print("\t" + repo_name + " repository already cloned, pulling...")

                    try: 

                        output = subprocess.check_output(git_pull, shell=True, stderr=subprocess.STDOUT)
                        print("\t" + output.decode('UTF-8').replace('\n', '\n\t'))

                    except subprocess.CalledProcessError as e:

                        print("\tCould not execute git pull...")
                        print("\t", e)

                except subprocess.CalledProcessError as e:

                    print("\t" + repo_name + " repository not present, cloning...")

                    try: 

                        output = subprocess.check_output(git_clone, shell=True, stderr=subprocess.STDOUT)
                        print("\t" + output.decode('UTF-8').replace('\n', '\n\t'))

                    except subprocess.CalledProcessError as e:

                        print("\tCould not execute git clone...")
                        print("\t", e)

                print("\n")
            
            end_time = time.time()
            elapsed_time = end_time - start_time

            print("\tExecuted in %.2f seconds\n" % elapsed_time )
            
        else:

            print("Found 0 public repositories for username", username,", exiting...")
            sys.exit(0)

    else:

        print("\n\t> Run the script with a valid path...")
        sys.exit(0)
    


if __name__ == '__main__':
    """Main function: args parsing and validation"""

    yes_answer = {'yes', 'y', 'ys', 'ye', ''}
    no_answer = {'no', 'n'}

    signal.signal(signal.SIGINT, signal_handler)

    is_git_installed = check_git()

    if(not(is_git_installed)):
        print("\n\tGit is not installed, exiting...")
        sys.exit(0)

    #Check for arguments length and content

    if (len(sys.argv) == 3):
        github_username = sys.argv[1]
        system_mirror_path = sys.argv[2]

        print("\n\tAre the following parameters correct?\n")
        print("\t\tGitHub username: ", github_username)
        print("\t\tSystem path to store mirrors:", system_mirror_path)

        print("\n\tAnswer[Yes/y/Y, No/n/N]: ", end='')
        answer = input().lower()
        
        if answer in yes_answer:
            print("\n\tProceeding to clone/pull public repositories of", github_username)

            do_mirror(
                github_username, 
                system_mirror_path
            )

        elif answer in no_answer:

            print("\n\tRun again with proper arguments:")
            print("\n\tpython git-mirror.py <GitHub username> <System path to store mirror>\n\n")
            sys.exit(0)

        else:

            print("Please answer with 'yes' or 'no'")
            sys.exit(0)

    else:

        print("\n\tRun the script with more arguments!")
        print("\n\tpython git-mirror.py <GitHub username> <System path to store mirror>\n\n")
        sys.exit(0)