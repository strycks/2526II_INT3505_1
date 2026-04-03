import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service(#{
  title: "Book Management API",
})
namespace Library;

model Book {
  id: int32;
  @minLength(1)
  title: string = "Dota's Dragon Blood";
  author: string = "valve, icefrog";
  year: int32 = 2026;
}

@route("/api/v1/books")
interface Books {
  @get
  list(): Book[];

  @post
  create(@body book: Book): { @statusCode statusCode: 201, @body body: Book };

  @route("/{id}")
  @get
  read(@path id: int32): Book | { @statusCode statusCode: 404 };

  @route("/{id}")
  @put
  update(@path id: int32, @body book: Book): Book;

  @route("/{id}")
  @patch
  patch(@path id: int32, @body book: Book): Book;

  @route("/{id}")
  @delete
  delete(@path id: int32): { @statusCode statusCode: 204 };
}