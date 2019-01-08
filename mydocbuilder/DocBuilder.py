# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3
from copy import deepcopy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE
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
                'register_list': self.register_list,
                'unregister_list': self.unregister_list,
                'monthly_report': self.monthly_report}
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

    def setMyFont(self, doc):
        """Set normal font of doc as my font."""
        doc.styles['Normal'].font.name = u'標楷體'
        doc.styles['Normal'].font.size = Pt(12)
        doc.styles['Normal']._element.rPr.rFonts.set(
                qn('w:eastAsia'), u'標楷體')

    def monthly_report(self):
        """Opens a copy of retire template, then modify and save it."""
        print('monthly_report_summary')
        filePath = ('./mydocbuilder/monthly_report_summary_template.docx')
        targetDoc = Document(filePath)
        # fill in the date
        replacements = {}
        today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
        today[0] = str(int(today[0]) - 1911) # in ROC year
        replacements['y'], replacements['m'], __ = today
        for p in targetDoc.paragraphs:
            if '{' in p.text:
                p.text = p.text.format(**replacements)
                break
        # fill in the categories
        con, cur = connect._get_connection()
        sqlstr = ('select description from hvhnonc_category')
        cur.execute(sqlstr)
        rows = cur.fetchall()
        rows = rows + [(u'合計',),]
        table = targetDoc.tables[0]
        for i, dataRow in enumerate(rows):
            try:
                tableRow = table.rows[i + 1]
            except IndexError:
                tableRow = table.add_row()
            tableRow.cells[0].text = dataRow[0]
        # set table font
        table = targetDoc.tables[0]
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    for run in paragraph.runs:
                        font = run.font
                        font.name = u'標楷體'
                        font.size = Pt(18)
                        run._element.rPr.rFonts.set(
                                qn('w:eastAsia'), u'標楷體')
        # set table style
        # TODO: line below not working
        #table.style = targetDoc.styles[WD_STYLE.TABLE_LIGHT_GRID]
        # save doc
        targetDoc.save('result.docx')

    def unregister_list(self):
        """Opens a copy of retire template, then modify and save it."""
        print('unregister_list')
        sourceDoc = Document('./mydocbuilder/retire_template.docx')
        targetDoc = Document('./mydocbuilder/retire_template.docx')
        self.setMyFont(targetDoc)
        # replacements.keys() = (dept, y, m, d, srl)
        replacements = {}
        replacements['dept'] = '秘書室'
        today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
        today[0] = str(int(today[0]) - 1911) # in ROC year
        replacements['y'], replacements['m'], replacements['d'] = today
        # replace 1st pages' line
        for paragraph in targetDoc.paragraphs:
            if '{' in paragraph.text:
                replacements['srl'] = '001'
                paragraph.text = paragraph.text.format(**replacements)
        # get data from sqlite db
        con, cur = connect._get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # columns: id, name, spec, unit, amount, acq date, keep year,
        #          used time, reason, comment, remark
        sqlstr = (
                'select '
                        'i.object_id as object_id, i.serial_id as serial_id, '
                        'i.name as name, i.spec as spec, i.unit as unit, '
                        'i.amount as amount, i.acquire_date as acquire_date, '
                        'i.keep_year as keep_year, '
                        'o.unregister_date as unregister_date, '
                        'o.reason as reason, '
                        'o.unregister_remark as unregister_remark '
                'from '
                        'hvhnonc_in as i '
                'inner join '
                        'hvhnonc_out as o '
                'on '
                        'i.id = o.in_id '
                'and '
                        '({conditions}1)') # e.g. '{cond1 and cond2 and }1'
        d = {'conditions': ''}
        params = []
        for k, v in self.kwargs.items():
            if 'date' in k:
                # date string tuple
                d['conditions'] += '({} between ? and ?) and '.format(k)
                params.extend(v)
            else:
                d['conditions'] += ('{} like ? and '.format(k))
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
                if not paragraph.text:
                    continue
                if '{' in paragraph.text:
                    p = targetDoc.add_paragraph(
                            paragraph.text.format(**replacements))
                    # insert table[0] (data table)
                    table = targetDoc.tables[0]
                    tbl = table._tbl
                    new_tbl = deepcopy(tbl)
                    p._p.addnext(new_tbl)
                    # a new empty line
                    p = targetDoc.add_paragraph()
                    # insert table[1] (signature table)
                    table = targetDoc.tables[1]
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
            # columns: id, name, spec, unit, amount, acq date, keep year,
            #          used time, reason, comment, remark
            # id
            wholeID = ' - '.join((row['object_id'], row['serial_id']))
            rowList.append(wholeID)
            # name, spec, unit, amount, price
            rowList.append(str(row['name']))
            rowList.append(str(row['spec']))
            rowList.append(str(row['unit']))
            rowList.append(str(row['amount']))
            # acq date
            y, m, d = map(int, row['acquire_date'].split('-'))
            y -= 1911 # in ROC years
            y, m, d = map(str, (y, m, d))
            date = '/'.join((y, m, d))
            rowList.append(str(date))
            # keep year
            rowList.append(str(row['keep_year']))
            # used time(in months) calculate in acquire and retire date
            acqY, acqM, acqD = map(int, row['acquire_date'].split('-'))
            retY, retM, retD = map(int, row['unregister_date'].split('-'))
            hasRemain = int(retD - acqD > 0)
            detY = retY - acqY
            detM = retM - acqM + hasRemain
            if detM < 0:
                detY -= 1
                detM += 12
            delta = (str(detY), str(detM))
            rowList.append('/'.join(delta))
            # reason, comment(empty), remark
            rowList.append(str(row['reason']))
            rowList.append('')
            rowList.append(str(row['unregister_remark']))
            # using the (i // rowPerPage * 2)th table
            tableIndex = i // rowPerPage * 2
            table = targetDoc.tables[tableIndex]
            # using the (i % rowPerPage + 1)th row (1st row is title)
            rowIndex = i % rowPerPage + 1
            try:
                tableRow = table.rows[rowIndex]
                for j, c in enumerate(tableRow.cells):
                    print('[{0}]:{1}'.format(j, rowList[j]), end='')
                    c.text = str(rowList[j])
            except IndexError:
                output = {'i': i, 'j': j, 'rowIndex': rowIndex,
                          'len(tableRow)': len(table.rows),
                          'len(rowCells)': len(tableRow.cells),
                          'len(rowList)': len(rowList)}
                print(output)
                input('error occured')
                raise IndexError
            print()
            print('table[', tableIndex, '], row[', rowIndex, '] done!')
        # save doc
        targetDoc.save('result.docx')

    def register_list(self):
        """Opens a copy of add template, then modify and save it."""
        print('register_list')
        sourceDoc = Document('./mydocbuilder/add_template.docx')
        targetDoc = Document('./mydocbuilder/add_template.docx')
        self.setMyFont(targetDoc)
        # a dictionary for replacing
        replacements = {}
        # department
        replacements['dept'] = '秘書室'
        # date
        today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
        today[0] = str(int(today[0]) - 1911) # in ROC year
        replacements['y'], replacements['m'], replacements['d'] = today
        # fill in 1st pages' line
        for paragraph in targetDoc.paragraphs:
            if '{' in paragraph.text:
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
                    '({conditions}1)') # e.g. '{cond1 and cond2 and }1'
        d = {'conditions': ''}
        params = []
        for k, v in self.kwargs.items():
            if 'date' in k:
                # date string tuple
                d['conditions'] += '({} between ? and ?) and '.format(k)
                params.extend(v)
            else:
                d['conditions'] += ('{} like ? and '.format(k))
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
                if not paragraph.text:
                    continue
                if u'中華民國' in paragraph.text:
                    p = targetDoc.add_paragraph(
                            paragraph.text.format(**replacements))
                    # insert table[0] (data table)
                    table = targetDoc.tables[0]
                    tbl = table._tbl
                    new_tbl = deepcopy(tbl)
                    p._p.addnext(new_tbl)
                    # a new empty line
                    p = targetDoc.add_paragraph()
                    # insert table[1] (signature table)
                    table = targetDoc.tables[1]
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
            wholeID = ' - '.join((row['object_id'], row['serial_id']))
            rowList.append(wholeID)
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
            tableIndex = i // rowPerPage * 2
            table = targetDoc.tables[tableIndex]
            # using the (i % rowPerPage + 1)th row (1st row is title)
            rowIndex = i % rowPerPage + 1
            try:
                tableRow = table.rows[rowIndex]
                for j, c in enumerate(tableRow.cells):
                    print('[{0}]:{1}'.format(j, rowList[j]), end='')
                    c.text = str(rowList[j])
            except IndexError:
                output = {'i': i, 'j': j, 'rowIndex': rowIndex,
                          'len(tableRow)': len(table.rows),
                          'len(rowCells)': len(tableRow.cells),
                          'len(rowList)': len(rowList)}
                print(output)
                input('error occured')
                raise IndexError
            print()
            print('table[', tableIndex, '], row[', rowIndex, '] done!')
        targetDoc.save('result.docx')


def main():
    myDocBuilder = DocBuilder()


if __name__ == '__main__':
    main()
