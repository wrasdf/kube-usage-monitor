### Goal of this repo

- Watch node usage
- Watch deployment top usage in cluster

### How to run
- $ docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ~/.kube:/root/.kube \
  -v $(pwd):/app \
  kube-monitor:latest python app/runner.py -n cpu_usage -t 10

### How to debug and run in container
- $ make sh
- $ make help
