lint:
	black .; isort .

local_run:
	uvicorn app.main:app --reload