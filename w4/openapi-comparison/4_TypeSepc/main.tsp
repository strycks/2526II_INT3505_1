import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;

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
}