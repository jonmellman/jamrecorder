DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -z "$(uname -a | grep raspberry)" ]]; then
	FLASK_APP=$DIR/jamrecorder.py MOCKS=true flask run
else
	FLASK_APP=$DIR/jamrecorder.py flask run --host=0.0.0.0
fi
