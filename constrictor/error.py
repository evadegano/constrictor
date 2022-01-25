class Error:
  def __init__(self, pos_start, pos_end, error_name, details):
    self.pos_start = pos_start
    self.pos_end = pos_end
    self.error_name = error_name
    self.details = details
  
  def as_string(self):
    result = f"{self.error_name}: {self.details} \nFile {self.pos_start.file_name}, line {self.pos_start.row + 1}"
    return result


class IllegalCharError(Error):
  def __init__(self, pos_start, pos_end, details):
    super().__init__(pos_start, pos_end, "Illegal Character", details)


# class to keep track of error position
class Position:
  def __init__(self, idx, row, col, file_name, file_txt):
    self.idx = idx
    self.row = row
    self.col = col
    self.file_name = file_name
    self.file_txt = file_txt

  # move to next index and update row and col number
  def advance(self, current_char):
    self.idx += 1
    self.col += 1

    # if line break, udpate row and col accordingly
    if current_char == "\n":
      self.row += 1
      self.col = 0

    return self

  # return copy of the position to keep track of start of error
  def copy(self):
    return Position(self.idx, self.row, self.col, self.file_name, self.file_txt)