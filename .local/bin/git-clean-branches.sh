#!/usr/bin/env sh

set -e

echo "Your branches"
git branch -a
echo

echo "Fetch remote branches"
git fetch --all
echo

echo "Prune remote branches"
git remote prune origin
echo

echo "Check local changes"
git add .
if [ -n "$(git diff --cached)" ]; then
    local_changes="true"
else
    local_changes="false"
fi
git reset
echo

if [ "$local_changes" = "false" ]; then
    echo "Switch to main and pull"
    git switch main
    git pull
else
    echo "You have local changes"
    echo "Skip witch to main"
fi
echo

echo "Delete local branches"
for b in `git branch --format='%(refname:short)' --merged main`; do
    if [ "$b" = "main" ] || [ "$b" = `git branch --show-current` ]; then
        continue
    fi
    git branch -D "$b"
done
echo

echo "Your branches"
git branch -a
