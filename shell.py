import constrictor.parser as parser

while True:
  text = input("Constrictor > ")
  result, error = parser.run("<stdin>", text)

  if error: print(error.as_string())
  else: print(result)