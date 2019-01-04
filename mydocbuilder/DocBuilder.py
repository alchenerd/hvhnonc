# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3
from copy import deepcopy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
import datetime
import sys

if __name__ == '__main__': # at mydocbuilder
    sys.path.append('../')

from myconnect import connect

class DocBuilder():
    """DocBuilder is a customized docx creator exclusively for hvhnonc."""
    def __init__(self, type_: str = 'default', **kwargs):
        self.actions = {
                'default': self.hello_docx,
                'register_list': self.register_list}
        if self.actions.get(type_, None):
            self.type_ = type_
        else:
            raise Exception('No such doc type.')
            self.type_ = 'default'
        self.kwargs = kwargs.get('kwargs')

    def construct(self):
        """Constructs a docx and save it."""
        #see self.actions for individual construct functions
        self.actions[self.type_]()

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
            document.save('result.docx')
        pass

    def register_list(self):
        """Opens a copy of register_list template, then modify and save it."""
        print('register_list')
        sourceDoc = Document('./mydocbuilder/add_template.docx')
        targetDoc = Document('./mydocbuilder/add_template.docx') # 1st page
        targetDoc.styles['Normal'].font.name = u'標楷體'
        targetDoc.styles['Normal'].font.size = Pt(12)
        targetDoc.styles['Normal']._element.rPr.rFonts.set(
                qn('w:eastAsia'), u'標楷體')
        # a dictionary for replacing
        replacements = {}
        # department
        replacements['dept'] = '秘書室'
        # date
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        today = today.split('-')
        today[0] = str(int(today[0]) - 1911) # in ROC year
        replacements['y'], replacements['m'], replacements['d'] = today
        # fill in 1st pages' line
        for paragraph in targetDoc.paragraphs:
            if u'中華民國' in paragraph.text:
                replacements['srl'] = '001'
                paragraph.text = paragraph.text.format(**replacements)
        # get data from sqlite db
        con, cur = connect._get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # columns: id, name, spec, unit, amount, price, total price, acq date,
        #          keep year, place, use department or keep department, keeper
        sqlstr = (
                'select '
                    'object_id, serial_id, name, spec, unit, amount, price, '
                    'acquire_date, keep_year, place, keep_department, keeper '
                'from '
                    'hvhnonc_in '
                'where '
                    '({condition}1)') # e.g. '{cond1 and cond2 and }1'
        d = {'condition': ''}
        params = []
        for k, v in self.kwargs.items():
            if 'date' in k:
                # date string tuple
                d['condition'] += '({} between ? and ?) and '.format(k)
                params.extend(v)
            else:
                d['condition'] += ('{} like ? and '.format(k))
                params.append(v)
        print('sqlstr:', sqlstr.format(**d), 'params:', params)
        cur.execute(sqlstr.format(**d), params)
        rows = cur.fetchall()
        con.close()
        # copy page by result row count(fill in dept, date and page serial)
        rowCount = len(rows)
        rowPerPage = 7
        pageCount = rowCount // rowPerPage + (rowCount % rowPerPage > 0)
        print(rowCount, 'rows, ', pageCount, 'pages.')
        # page copying
        for i in range(1, pageCount): # from page 2 to pageCount
            # serial(dynamically changes each page)
            replacements['srl'] = str(i + 1).zfill(3)
            if i < pageCount:
                targetDoc.add_page_break()
            for paragraph in sourceDoc.paragraphs:
                # copy paragraphs
                # check for replacement
                if u'中華民國' in paragraph.text:
                    p = targetDoc.add_paragraph(
                            paragraph.text.format(**replacements))
                    # insert the table in a new paragraph
                    # copy the tables
                    table = targetDoc.tables[0]
                    tbl = table._tbl
                    new_tbl = deepcopy(tbl)
                    p._p.addnext(new_tbl)
                else:
                    p = targetDoc.add_paragraph(paragraph.text)
                p.paragraph_format.alignment = \
                        paragraph.paragraph_format.alignment
        # write in the data
        for i, row in enumerate(rows):
            # prepare list
            rowList = []
            # columns: id, name, spec, unit, amount, price, total price,
            #          acq date, keep year, place,
            #          use department or keep department, keeper
            # id
            rowList.append(
                    str(' - '.join((row['object_id'], row['serial_id']))))
            # name, spec, unit, amount, price
            rowList.append(str(row['name']))
            rowList.append(str(row['spec']))
            rowList.append(str(row['unit']))
            rowList.append(str(row['amount']))
            rowList.append(str(row['price']))
            # total price
            totalPrice = int(row['amount']) * int(row['price'])
            rowList.append(str(totalPrice))
            # acq date
            y, m, d = map(int, row['acquire_date'].split('-'))
            y -= 1911 # in ROC years
            y, m, d = map(str, (y,m,d))
            date = '/'.join((y,m,d))
            rowList.append(str(date))
            # keep year, place, use department or keep department, keeper
            rowList.append(str(row['keep_year']))
            rowList.append(str(row['place']))
            rowList.append(str(row['keep_department']))
            rowList.append(str(row['keeper']))
            # using the (i // rowPerPage * 2)th table
            tableIndex = i // rowPerPage
            table = targetDoc.tables[tableIndex]
            # using the (i % rowPerPage + 1)th row
            rowIndex = i % rowPerPage + 1
            try:
                tableRow = table.rows[rowIndex]
            except IndexError:
                print(i, rowIndex, len(table.rows))
                #raise IndexError
            for j, c in enumerate(tableRow.cells):
                print('[{0}]:{1}'.format(j, rowList[j]), end='')
                c.text = str(rowList[j])
            print()
            print('table[', tableIndex, '], row[', rowIndex, '] done!')
        # print result to table
        targetDoc.save('result.docx')


def main():
    myDocBuilder = DocBuilder()


if __name__ == '__main__':
    main()
