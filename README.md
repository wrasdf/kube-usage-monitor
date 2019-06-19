### Goal of this repo

- Watch node usage
- Watch deployment top usage
- Support different env

### How to run
Step1: Update Env Data (And Cache to local)
```
make update-europa-stg
```
Step2: Print sorted nodes usage data
```
docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ~/.kube:/root/.kube \
  -v $(pwd):/app \
  kube-monitor:latest python app/runner.py \
  -e europa-stg \
  -n cpu_usage \
  -t 20
```

Or Step2: Print sorted pods usage data
```
docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ~/.kube:/root/.kube \
  -v $(pwd):/app \
  kube-monitor:latest python app/runner.py \
  -e europa-stg \
  -p cpu_request \
  -t 20
```

### How to debug and run in container
- $ make sh
- $ make help
