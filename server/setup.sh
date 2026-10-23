python3 -m venv venv &&
./venv/bin/pip install "transformers[torch]==4.48.*" bitsandbytes accelerate fastapi uvicorn &&
echo "Virtual environment set up, use \`source ./venv/bin/activate\` to enter the virtual environment. Then run \`python3 server.py\` to start the server"
