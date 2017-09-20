import git
from datetime import datetime
from threading import Timer
from csv import DictReader

def clone_repos():
    clone_location = "assignments"
    assignment_repos = []

    # load assignment <-> repository url association from file
    with open('assignment_repos.csv') as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        for row in reader:
            assignment_repos.append(row)

    if not assignment_repos:
        log_and_print("There are no valid repositories.")
        return

    log_and_print('Starting clone process..')
    for repo in assignment_repos:
        repo_url = 'http://github.com/' + repo['github_user'] + '/' + repo['repo'] + '.git'
        status = 'Cloning ' + repo_url + ' to '+ clone_location+'/'+repo['shortname']
        log_and_print(status)

        # continue even if  clone fails
        try:
            git.Git().clone(repo_url, clone_location+'/'+repo['shortname'])
            log_and_print('Success.')
        except:
            log_and_print('Cloning repository for ' + repo['shortname'] + ' failed.')

    log_and_print('Done.')


def log_and_print(message):
    timestamp = datetime.now().isoformat()
    log_entry = timestamp + ': ' + message
    with open('timed_clone.log', 'a') as logfile:
        logfile.write(log_entry+'\n')
    print(log_entry)


# deadline = "01.10.2017 - 00:05"
deadline = "20.09.2017 - 11:31"
now = datetime.now()
run_at = datetime.strptime(deadline, "%d.%m.%Y - %H:%M")
delay = (run_at - now).total_seconds()

log_and_print('Deadline set to: '+deadline)

if delay < 0:
    log_and_print('Deadline is in the past! - Running now.')
    clone_repos()
else:
    log_and_print('Delaying until deadline.')
    Timer(delay, clone_repos).start()