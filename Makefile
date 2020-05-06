# image tag parameter
TAG?=latest
build-es-image:
	docker build -t es7:$(TAG) --file ./dockerfiles/elasticsearch/Dockerfile .

create-ec2:
	python ./src/scripts/aws_ec2.py
