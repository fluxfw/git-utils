#!/usr/bin/env sh

set -e

path="$1"
if [ -z "$path" ]; then
    echo "Please pass a path" >&2
    exit 1
fi

echo "Your branches"
git -C "$path" branch -a
echo

echo "Fetch remote branches"
git -C "$path" fetch --all
echo

echo "Prune remote branches"
git -C "$path" remote prune origin
echo

echo "Check local changes"
git -C "$path" add .
if [ -n "$(git -C "$path" diff --cached)" ]; then
    local_changes="true"
else
    local_changes="false"
fi
git -C "$path" reset
echo

if [ "$local_changes" = "false" ]; then
    echo "Switch to main and pull"
    git -C "$path" switch main
    git -C "$path" pull
else
    echo "You have local changes"
    echo "Skip witch to main"
fi
echo

echo "Delete local branches"
for b in `git -C "$path" branch --format='%(refname:short)' --merged main`; do
    if [ "$b" = "main" ] || [ "$b" = `git -C "$path" branch --show-current` ]; then
        continue
    fi
    git -C "$path" branch -D "$b"
done
echo

echo "Your branches"
git -C "$path" branch -a
