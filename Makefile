upload-photos:
	rclone copy ./photos b2:ssvproff-media/photos/`date +%Y`/ --progress

upload-videos:
	rclone sync ./videos b2:ssvproff-media/videos/ --progress

push-data:
	dvc push

docs-serve:
	mkdocs serve -a 0.0.0.0:8000

# --- API / WEB ---
api-dev:
	uvicorn app.main:app --reload --port 8001 --app-dir api

web-dev:
	cd web && npm run dev

web-build:
	cd web && npm run build

format:
	echo "Добавьте линтеры/форматтеры (ruff/black/eslint/prettier) по желанию"

# --- DATA / CLOUD ---
rclone-check:
	rclone ls b2:ssvproff-media || echo "Проверьте rclone config и креды"

dvc-config:
	bash flows/dvc-remote-example.sh

# --- DOCS ---
docs-build:
	mkdocs build --strict
