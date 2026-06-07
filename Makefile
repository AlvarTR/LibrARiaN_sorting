
MAKEFILE_DIR:=$(dir $(realpath $(lastword ${MAKEFILE_LIST})))


.venv ${MAKEFILE_DIR}.venv: 
	python3 -m venv ${MAKEFILE_DIR}.venv

pip_install: | .venv
	bash -c "source ${MAKEFILE_DIR}.venv/bin/activate && pip install -r ${MAKEFILE_DIR}requirements.txt"

run: | .venv
	bash -c "source ${MAKEFILE_DIR}.venv/bin/activate && python ${MAKEFILE_DIR}src/with_sorting.py"
