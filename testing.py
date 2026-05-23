posts: list[dict] = [
  {
  "id": 100,
  "author": "Opeyemi",
  "title": "Having money is not the problem",
  "content": "Not everyone will be rich",
  "date-posted": "June 10 2030",
},

{
  "id": 100,
  "author": "Abdulsalam",
  "title": "Love is the root of being poor",
  "content": "Not everyone will be rich",
  "date_posted": "June 10 2035",
}
]

name = posts[0]
# print(name.get("author"))

number = 99

message = ("opeyemi is a boy" if number > 100 else "opeyemi is a girl")

# print(message)

#  @app.get("/me2/{fire}")
# def get_return(fire: int):
#   for c in posts:
#     if c.get("id") == fire:
#       return c
#   return { 
#     "status_code": 400, 
#     "content": {"error": "post not found"} 
#     },

# return JSONResponse( status_code=404, content={"error": "Post not found"} ),
# return { "status_code": 400, "content": {"error": "post not found"} },



class Named:
  def __init__(self, name, age) -> None:
    self.name = name
    self.age = age


  @property
  def naming(self):
    if self.name:
      return self.name
    return "This is gaven name"

new_user = Named(name="opeyemi", age=25)
print(new_user.naming)

import secrets

print(secrets.token_hex(27))