TESTS_PREP_SCRIPT=./tests/setup_scripts/rerun_prep.py
TESTS_RESULTS_SCRIPT=./tests/setup_scripts/rerun_results.py
TESTS_CLEAN_SCRIPT=./tests/setup_scripts/clean.py


help:
	@echo 'Makefile for vak                                                                 '
	@echo '                                                                                 '
	@echo 'Usage:                                                                           '
	@echo '   make tests-setup                          generate test data used by tests    '
	@echo '   make tests-clean                          remove generated test data          '

variables:
	@echo '     TESTS_PREP_SCRIPT       : $(TESTS_PREP_SCRIPT)          '
	@echo '     TESTS_RESULTS_SCRIPT    : $(TESTS_RESULTS_SCRIPT)       '
	@echo '     TESTS_CLEAN_SCRIPT      : $(TESTS_CLEAN_SCRIPT)         '

tests-setup : $(TESTS_PREP_SCRIPT) $(TESTS_RESULTS_SCRIPT)
	python $(TESTS_PREP_SCRIPT)
	python $(TESTS_RESULTS_SCRIPT)

tests-clean :
	python $(TESTS_CLEAN_SCRIPT)


.PHONY: help variables tests-setup tests-clean
