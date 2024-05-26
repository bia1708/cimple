#!/bin/bash
# Get primary language from repo (i.e. cimple's would be Python)

repo=$1

repo_name=$(echo "$repo" | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link
repo_owner=$(echo "$repo" | awk -F'/' '{print $4}')

supported_languages=",Python,Java,C++,"

# Extract repo languages with their number of bytes
languages=$(gh api repos/"$repo_owner"/"$repo_name"/languages | jq -r 'to_entries|map("\(.key):\(.value)")|.[]')

max_bytes=0
# Find the language that has the maximum bytes and is one of the supported languages
for lang_entry in $languages; do
    lang=$(echo "$lang_entry" | cut -d: -f1)
    bytes=$(echo "$lang_entry" | cut -d: -f2)

    if [ "$(echo "$supported_languages" | grep ",$lang,")" != "" ] && [[ $bytes > $max_bytes ]]; then
        max_bytes=$bytes
        primary_language="$lang"
        break
    fi
done

echo "language:$primary_language"