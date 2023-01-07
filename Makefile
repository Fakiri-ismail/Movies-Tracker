format:
	black .
	isort -rc .
	autoflake .
test:
	pytest .