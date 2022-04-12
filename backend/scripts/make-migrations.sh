docker compose exec --workdir="/app/belay_me/migrations" api_tests alembic revision --autogenerate -m "${1}"
