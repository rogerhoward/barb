import config
import git 

# Digital Ocean instance lists
def consider(message):
    """Git: attempts to git pull the current project.

    Return: Status message, or False.
    """
    if config.log: print('git pull considered')
    possible_trigger = '{} git pull'.format(message['trigger_word'])
    if message['text'].startswith(possible_trigger):
        if config.log: print('git pull triggered')
        g = git.cmd.Git(config.project_directory)
        g.pull()
        return 'git pulled'
    else:
        return False