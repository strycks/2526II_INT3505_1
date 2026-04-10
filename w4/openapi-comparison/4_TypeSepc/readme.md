1. Install dependencies: `tsp install`
2. Compile: `tsp compile .`
3. The YAML file rendered is found in `\tsp-output\openapi.yaml`
4. Generate server code `openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./out/python-server`