install:
	python3 -m venv virt_env
	virt_env/bin/pip install -r requirments.txt

run:
	virt_env/bin/python3 a_maze_ing.py config.txt

debug:
	virt_env/bin/python3 -m pdb -m a_maze_ing

clean:
	
# https://earthly.dev/blog/python-makefile/

lint:
	