import constrictor.lexer as lexer

while True:
  text = input("Constrictor > ")
  result, error = lexer.run("<stdin>", text)

  if error: print(error.as_string())
  else: print(result)