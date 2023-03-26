OK_MSG = \x1b[32m ✔\x1b[0m
SHELL=bash

test: lint unittest
	@echo -e "All tests complete $(OK_MSG)"

fmt:
	@echo -n "==> Checking that code is autoformatted with black..."
	@.venv/bin/python -m black  --exclude '(.venv|vendor)' .
	@echo -e "$(OK_MSG)"

lint:
	@echo -n "==> Running flake8..."
	@.venv/bin/flake8 --show-source --exclude=.venv
	@echo -e "$(OK_MSG)"


unittest:
	@echo "==> Running tests..."
	@PYTHONPATH=. .venv/bin/pytest ./test --cov-report term-missing:skip-covered  --no-cov-on-fail -W ignore::DeprecationWarning -vv

env:
	@echo "==> Creating virtualenv..."
	test -d .venv || python3 -m venv .venv
	# build wheels when developing locally
	test -z "$$CI" && .venv/bin/pip install -U pip wheel || true
	brew install portaudio ffmpeg
	.venv/bin/pip install -r requirements.txt 
	.venv/bin/pip install -r requirements-dev.txt 
	touch .venv
	source .venv/bin/activate

clean:
	rm -rf .venv


%: %-default
	@ true