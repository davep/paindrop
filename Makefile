###############################################################################
# Common make values.
app      := paindrop
src      := src/$(app)
run      := rye run
python   := $(run) python
lint     := rye lint
mypy     := $(run) mypy

##############################################################################
# Run the app.
.PHONY: run
run:
	$(python) -m $(app)

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Install all dependencies
	rye sync
#	$(run) pre-commit install

##############################################################################
# Checking/testing/linting/etc.
.PHONY: lint
lint:				# Run Pylint over the library
	$(lint) $(src)

.PHONY: typecheck
typecheck:			# Perform static type checks with mypy
	$(mypy) --scripts-are-modules $(src)

.PHONY: stricttypecheck
stricttypecheck:	        # Perform a strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(src)

.PHONY: checkall
checkall: lint stricttypecheck test # Check all the things

##############################################################################
# Package/publish.
.PHONY: package
package:			# Package the library
	rye build

.PHONY: spackage
spackage:			# Create a source package for the library
	rye build --sdist

.PHONY: packagecheck
packagecheck: package spackage		# Check the packaging.
	$(twine) check dist/*

.PHONY: testdist
testdist: packagecheck		# Perform a test distribution
	rye publish --repository testpypi --repository-url https://test.pypi.org/legacy/

.PHONY: dist
dist: packagecheck		# Upload to pypi
	rye publish

##############################################################################
# Utility.
.PHONY: ugly
ugly:				# Reformat the code with black.
	rye fmt $(src)

.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: clean
clean:				# Clean the build directories
	rm -rf dist

.PHONY: help
help:				# Display this help
	@grep -Eh "^[a-z]+:.+# " $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.+# "}; {printf "%-20s %s\n", $$1, $$2}'

##############################################################################
# Housekeeping tasks.
.PHONY: housekeeping
housekeeping:			# Perform some git housekeeping
	git fsck
	git gc --aggressive
	git remote update --prune

### Makefile ends here
