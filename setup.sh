docker build -t mcprep-helpful-horse-docker .
docker run -d --restart unless-stopped --name mcprep-helpful-horse mcprep-helpful-horse-docker:latest
