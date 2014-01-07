pip install snakeviz

python -m cProfile -s time -o thing.txt Controller.py

snakeviz thing.txt