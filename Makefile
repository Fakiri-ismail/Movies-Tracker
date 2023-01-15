format:
	black .
	isort -rc .
	autoflake .
tests:
	pytest .
generate-docs:
	pdoc3 --html --force api