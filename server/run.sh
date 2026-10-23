if [ ! -d "$./venv" ]; then
	bash ./setup.sh
fi

echo "Starting server."
$(source ./venv/bin/activate; python3 server.py)
