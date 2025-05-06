docker build -t paisa-agent .
docker remove paisa-agent -f
docker run --name paisa-agent --add-host=host.docker.internal:host-gateway --env-file .env -p 8002:8002 -d paisa-agent