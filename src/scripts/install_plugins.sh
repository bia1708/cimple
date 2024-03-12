#!/bin/bash

jnlp=$1
url=$2

java -jar $jnlp -s $url -webSocket install-plugin <name>