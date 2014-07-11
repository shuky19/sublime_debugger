#!/bin/bash

RUBY_EXECUTABLE=$1
DEBUG_LOGS_ENABLED=$2

if [[ $DEBUG_LOGS_ENABLED = "True" ]]; then
	echo
	echo "----------------------------------------"
	echo "------------Ruby Executor---------------"
	echo "----------------------------------------"
fi

if [[ $RUBY_EXECUTABLE = "rvm" ]]; then
	# Initialize RVM
	[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

	if [[ $DEBUG_LOGS_ENABLED = "True" ]]; then
		echo "Method: RVM"
		echo -n "Using ruby version: "; echo | ruby --version;
		echo -n "Located at: " ; echo | which ruby
		echo -n "Ruby Arguments = "
		echo "$3" "$4" "$5" "$6" "$7"
		echo
	fi

	# Run ruby
	ruby "$3" "$4" "$5" "$6" "$7"
elif [[ $RUBY_EXECUTABLE = "rbenv" ]]; then
	# Initialize rbenv
	if [ -d $HOME/.rbenv ]; then
	  export PATH="$HOME/.rbenv/bin:$PATH"
	  eval "$(rbenv init -)"
	fi

	if [[ $DEBUG_LOGS_ENABLED = "True" ]]; then
		echo "Method: rbenv"
		echo -n "Using ruby version: "; echo | ruby --version
		echo -n "Located at: " ; echo | which ruby
		echo -n "Ruby Arguments = "
		echo "$3" "$4" "$5" "$6" "$7"
		echo
	fi

	# Run ruby
	ruby "$3" "$4" "$5" "$6" "$7"
else
	if [[ $DEBUG_LOGS_ENABLED = "True" ]]; then
		echo "Using ruby binary from: $RUBY_EXECUTABLE"
		echo -n "Ruby Arguments = "
		echo "$3" "$4" "$5" "$6" "$7"
		echo
	fi

	eval "$RUBY_EXECUTABLE \"\$3\" \"\$4\" \"\$5\" \"\$6\" \"\$7\""
fi