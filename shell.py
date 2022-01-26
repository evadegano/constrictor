import constrictor.app as app

while True:
  text = input("Constrictor > ")
  result, error = app.run("<stdin>", text)

  if error: print(error.as_string())
  else: print(result)