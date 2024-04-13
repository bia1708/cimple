.PHONY: install run

install:
	# Install APT dependencies
	#sudo apt-get update
	#sudo apt-get install -y curl jq gh
	pip install -r requirements.txt
	# Install npm
	# sudo apt-get install -y npm

	#TODO: Install npm dependencies

run:
	python3 main.py