from constrictor.helpers import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}"
        result += f"\nFile {self.pos_start.file_name}, line {self.pos_start.row + 1}"
        result += f"\n\n {string_with_arrows(self.pos_start.file_txt, self.pos_start, self.pos_end)}"

        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class RuntimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += f"\n\n {string_with_arrows(self.pos_start.file_txt, self.pos_start, self.pos_end)}"

        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        context = self.context

        while context:
            result = (
                f"  File {pos.file_name}, line {str(pos.row + 1)}, in {context.display_name}\n"
                + result
            )
            pos = context.parent_entry_pos
            context = context.parent

        return "Traceback (most recent call last):\n" + result


# class to keep track of error position
class Position:
    def __init__(self, idx, row, col, file_name, file_txt):
        self.idx = idx
        self.row = row
        self.col = col
        self.file_name = file_name
        self.file_txt = file_txt

    # move to next index and update row and col number
    def advance(self, current_char=None):
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
