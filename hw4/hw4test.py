"""
A test of TxtFileHandler class.
"""

from hw4 import TxtFileHandler


file_path = "test.txt"
handler = TxtFileHandler(file_path)

handler.write_file("Hello", "World", encoding="utf-8")

handler.append_file("1111111Hello", "111111World", encoding="utf-8")

print(handler.read_file(encoding="utf-8"))