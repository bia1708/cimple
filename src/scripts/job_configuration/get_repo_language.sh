#!/bin/bash

username=$1
repo=$2

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

repo_owner=$(echo $repo | awk -F'/' '{print $4}')

# Get primary language from repo (i.e. cimple's would be Python)
#language=`gh api repos/$repo_owner/$repo_name/languages | jq 'to_entries | max_by(.value) | .key'`

languages=$(gh api repos/$repo_owner/$repo_name/languages)

# Extract the language with the highest number of bytes of code
primary_language=$(echo "$languages" | jq -r 'to_entries | max_by(.value) | .key')

# Prioritization order (so as not to wrongly interpret language)
declare -A language_priority=(
    ["Python"]=1
    ["Java"]=2
    ["C++"]=3
    ["JavaScript"]=4
    ["Ruby"]=5
    ["CSS"]=99
)

# Function to get the highest priority language
get_highest_priority_language() {
    echo "$languages" | jq -r 'to_entries | .[] | @base64' | while read entry; do
        _jq() {
            echo ${entry} | base64 --decode | jq -r ${1}
        }
        lang=$(_jq '.key')
        bytes=$(_jq '.value')
        priority=${language_priority[$lang]:-100}
        # Multiply bytes by -1 to sort in descending order
        echo "$((bytes * -1)) $priority $lang"
    done | sort -n | head -n 1 | cut -d' ' -f3
}
    # echo "$languages" | jq -r 'to_entries | .[] | .key' | while read lang; do
    #     priority=${language_priority[$lang]:-100}
    #     echo "$priority $lang"
    # done | sort -n | head -n 1 | cut -d' ' -f2
# }

# Determine the primary language
if [ -n "$primary_language" ]; then
    primary_language=$(get_highest_priority_language)
fi

echo "language:$primary_language"