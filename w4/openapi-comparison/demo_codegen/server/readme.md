1. Install code generator via NPM:  
```
npm install @openapitools/openapi-generator-cli -g
```
2. Run the following commands to generate server code based on specification:
```
openapi-generator-cli generate -i demo.yaml -g python-flask -o ./out/python-server
```
3. Refer to the README.md file in `/out/` for further steps.