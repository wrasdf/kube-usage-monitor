### Goal of this repo

- Watch node usage
- Watch deployment top usage
- Support different env

### How to run
- $ docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ~/.kube:/root/.kube \
  -v $(pwd):/app \
  kube-monitor:latest python app/runner.py -e europa-stg -c true -n cpu_usage -t 10

### How to debug and run in container
- $ make sh
- $ make help
