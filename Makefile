# ==========================================
# N100 Financial Intelligence Platform
# Makefile
# ==========================================

load:
	python src/etl/load_database.py

validate:
	python src/etl/validator.py

test:
	python -m pytest -v

report:
	python src/etl/review_summary.py

dashboard:
	@echo Dashboard module will be implemented in a later sprint.

api:
	@echo API module will be implemented in a later sprint.

ratios:
	python src/analytics/kpi_engine.py

clean:
	@echo Cleaning output folder...