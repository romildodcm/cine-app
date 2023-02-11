echo "Inicializando backend..."
cd ./backend
source venv/bin/activate
export PYTHONPATH=.
uvicorn main:app --reload --host
