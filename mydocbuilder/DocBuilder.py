# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""

from docx import Document

class DocBuilder():
    """DocBuilder is a customized docx creator exclusively for hvhnonc."""
    def __init__(self, type_: str = 'default', **kwargs):
        self.kwargs = dict(kwargs)
        actions = {'default': self.hello_docx}
        # Call the designated function with type_ parameter
        actions[type_]()

    def hello_docx(self):
        """Makes a dummy hello docx document."""
        document = Document()
        document.add_heading('Hello .docx!', 0)
        p = document.add_paragraph('This is my test paragraph!')
        records = ((2,9,4),(7,5,3),(6,1,8))
        table = document.add_table(rows=0, cols=3)
        for x, y, z in records:
            rowCells = table.add_row().cells
            rowCells[0].text = str(x)
            rowCells[1].text = str(y)
            rowCells[2].text = str(z)
            document.save('hello_docx.docx')
        pass


def main():
    myDocBuilder = DocBuilder()


if __name__ == '__main__':
    main()
