# Rebuild the site locally.
python3 -m src.main
# Serve the generated docs directory for local preview.
cd docs && python3 -m http.server 8888
