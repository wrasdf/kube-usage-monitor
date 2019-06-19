# python test
build:
	@docker build -t kube-monitor:latest .

sh: build
	@docker run --rm -it \
		-v $(HOME)/.aws:/root/.aws \
		-v $(HOME)/.kube:/root/.kube \
		-v $$(pwd):/app \
		--entrypoint "/bin/sh" \
		kube-monitor:latest

help:
	echo "docker run --rm -it -v ~/.kube:/root/.kube -v $$(pwd):/app kube-monitor:latest python app/runner.py args..."
	@docker run --rm \
		-v $(HOME)/.aws:/root/.aws \
		-v $(HOME)/.kube:/root/.kube \
		-v $$(pwd):/app \
		kube-monitor:latest python app/runner.py --help

update-%:
	@docker run --rm -t \
		-v $(HOME)/.aws:/root/.aws \
		-v $(HOME)/.kube:/root/.kube \
		-v $$(pwd):/app \
		kube-monitor:latest python app/runner.py -e $(*) -c true
