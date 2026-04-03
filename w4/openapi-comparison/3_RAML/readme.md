1. Install ram2html: `npm install -g raml2html`
2. Export to html: `raml2html raml.raml > index.html`
3. Open `index.html` to view documentation.
4. Install oas-raml-converter `npm i -g oas-raml-converter`
5. Convert to OpenAPI Spec `oas-raml-converter --from RAML --to OAS30 raml.raml > swagger.json`
6. Install openapi-generator-cli `npm install @openapitools/openapi-generator-cli -g`
7. Generate server code `openapi-generator-cli generate -i swagger.json -g python-flask -o ./out/python-server`