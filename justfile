build-and-test: build-image test-image

build-image:
	podman build -t mcprep-helpful-horse-docker .

test-image:
	podman run --name mcprep-helpful-horse mcprep-helpful-horse-docker:latest
