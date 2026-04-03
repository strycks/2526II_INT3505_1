1. Install Aglio: `npm install -g aglio`
2. Run preview: `aglio -i api-bp.apib -s`
3. Open in browser: `http://localhost:3000`
4. Install apib2openapi `npm install -g apib2openapi`
5. Convert to OpenAPI Spec `apib2openapi -i api-bp.apib -y -o swagger.yaml`
6. Generate code `openapi-generator-cli generate -i swagger.yaml -g python-flask -o ./out/python-server`