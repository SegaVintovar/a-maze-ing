install:
	python3 -m venv virt_env
	virt_env/bin/python3 -m pip install -r requirments.txt

run:
	virt_env/bin/python3 a_maze_ing.py config.txt

debug:
	virt_env/bin/python3 -m pdb -m a_maze_ing config.txt

clean:
	rm -rf __pycache__/
	rm -rf .mypy_cache/
# https://earthly.dev/blog/python-makefile/

lint:
# 	python3 -m flake8 . we need to make it work
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs
