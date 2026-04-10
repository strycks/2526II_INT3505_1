1. Install Aglio: `npm install -g aglio`
2. Run preview: `aglio -i api-bp.apib -s`
3. Open in browser: `http://localhost:3000`
4. Convert to OpenAPI Spec: `npm install -g apib2openapi` and then `apib2openapi -i api-bp.apib -o swagger.yaml --yaml`
5. Generate server code `openapi-generator-cli generate -i swagger.yaml -g python-flask -o ./out/python-server`