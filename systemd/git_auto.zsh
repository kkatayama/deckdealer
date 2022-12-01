#!/usr/bin/zsh
#
# Script to run every 5 minutes (cronjob)
# 0. Navigate to Backend Directory
# 1. fetch and pull updates from github
# 2. add and commit any backend updates (log files, database file, etc...)
# 3. push backend changes

BACKEND=$HOME/Documents/DeckDealer/deckdealer

# -- 0. Navigate to Backend Directory
RUN_TIME=$(/bin/date "+%Y-%m-%d %I:%M:%S")
echo "\nRun Time: ${RUN_TIME}\n" >> "${BACKEND}/logs/git_auto.log"

cmd=(cd "${BACKEND}")
echo "${cmd}" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"

# -- 1. fetch and pull updates from github
cmd=(git fetch)
echo "${cmd}" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"

cmd=(git pull)
echo "${cmd}" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"


# -- 2. add and commit any backend updates (log files, database file, etc...)
cmd=(git add -A)
echo "${cmd}" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"

cmd=(git commit -am 'git auto update')
echo "git commit -am 'git auto update'" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"

# -- 3. push backend changes
cmd=(git push)
echo "${cmd}" >> "${BACKEND}/logs/git_auto.log"
$cmd >> "${BACKEND}/logs/git_auto.log"
