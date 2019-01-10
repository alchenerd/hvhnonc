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
from docx.enum.style import WD_STYLE_TYPE
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
        """Opens monthly report template, then modify and save it."""
        print('monthly_report_summary')
        filePath = ('./mydocbuilder/monthly_report_summary_template.docx')
        targetDoc = Document(filePath)
        # get the month
        edmin, edmax = self.kwargs.get('acquire_date', (None, None))
        if edmin:
            theYear, theMonth = edmin.year, edmin.month
        elif edmax:
            theYear, theMonth = edmax.year, edmax.month
        else:
            today = datetime.datetime.today()
            theYear, theMonth = today.year, today.month
        # fill in the date
        replacements = {}
        replacements['y'] = str(theYear - 1911) # in ROC year
        replacements['m'] = str(theMonth).zfill(2)
        for p in targetDoc.paragraphs:
            if '{' in p.text:
                p.text = p.text.format(**replacements)
                for run in p.runs:
                    font = run.font
                    font.name = u'標楷體'
                    font.size = Pt(16)
                    run._element.rPr.rFonts.set(
                    qn('w:eastAsia'), u'標楷體')
                    break
        # init connection (tag: $$$)
        con, cur = connect._get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # get registered $ before the month
        sqlstr = ('select amount, price, category '
                  'from hvhnonc_in '
                  'where acquire_date < ?')
        params = ('-'.join((str(theYear).zfill(4), str(theMonth).zfill(2),
                            '01')),)
        inPreMonth = cur.execute(sqlstr, params).fetchall()
        pricePreMonth = {}
        for row in inPreMonth:
            # init if category not in keys
            if row['category'] not in pricePreMonth.keys():
                pricePreMonth[row['category']] = 0
            pricePreMonth[row['category']] += row['price'] * row['amount']
        sqlstr = ('select '
                      'o.amount as amount, '
                      'i.price as price, '
                      'i.category as category '
                  'from hvhnonc_in as i '
                  'inner join hvhnonc_out as o '
                  'on i.id = o.in_id '
                  'and o.unregister_date < ?')
        outPreMonth = cur.execute(sqlstr, params).fetchall()
        for row in outPreMonth:
            # init if category not in keys
            if row['category'] not in pricePreMonth.keys():
                pricePreMonth[row['category']] = 0
            pricePreMonth[row['category']] -= row['price'] * row['amount']
        # get registered $ in the month
        sqlstr = ('select amount, price, category '
                  'from hvhnonc_in '
                  'where acquire_date '
                  'between date(:d, "start of month") '
                  'and date(:d, "start of month", "+1 month", "-1 day")')
        params = {'d': '-'.join((str(theYear).zfill(2), str(theMonth).zfill(2),
                                 '15'))}
        dataInMonth = cur.execute(sqlstr, params).fetchall()
        priceInMonth = {}
        for row in dataInMonth:
            # init if category not in keys
            if row['category'] not in priceInMonth.keys():
                priceInMonth[row['category']] = 0
            priceInMonth[row['category']] += row['price'] * row['amount']
        # get unregistered $ in the month
        sqlstr = ('select '
                      'o.amount as amount, '
                      'i.price as price, '
                      'i.category as category '
                  'from hvhnonc_in as i '
                  'inner join hvhnonc_out as o '
                  'on ((i.id = o.in_id) '
                  'and (o.unregister_date '
                  'between date(:d, "start of month") '
                  'and date(:d, "start of month", "+1 month", "-1 day")))')
        params = {'d': '-'.join((str(theYear).zfill(2), str(theMonth).zfill(2),
                                 '15'))}
        dataOutMonth = cur.execute(sqlstr, params).fetchall()
        priceOutMonth = {}
        for row in dataOutMonth:
            # init if category not in keys
            if row['category'] not in priceOutMonth.keys():
                priceOutMonth[row['category']] = 0
            priceOutMonth[row['category']] += row['price'] * row['amount']
        # teardown connection (tag: $$$)
        con.close()
        # fill in data
        table = targetDoc.tables[0]
        for rc, row in enumerate(table.rows):
            if rc == 0:
                continue
            category = row.cells[0].text
            # cells[1]: price pre month
            ppm = pricePreMonth.get(category, None)
            row.cells[1].text = str(ppm) if ppm else ''
            # cells[2]: price in month
            pim = priceInMonth.get(category, None)
            row.cells[2].text = str(pim) if pim else ''
            # cells[3]: price out month
            pom = priceOutMonth.get(category, None)
            row.cells[3].text = str(pom) if pom else ''
            # cells[4]: sum
            sum_ = ppm if ppm else 0
            sum_ += pim if pim else 0
            sum_ -= pom if pom else 0
            row.cells[4].text = str(sum_) if sum_ else ''
            # last row: sum
            if rc == len(table.rows) - 1:
                for cc, cell in enumerate(row.cells):
                    if cc in (0, 5):
                        continue
                    toSum = \
                        [table.rows[x].cells[cc].text for x in range(1, rc)]
                    toSum = [int(x) for x in toSum if x]
                    if not len(toSum):
                        cell.text = ''
                    else:
                        cell.text = str(sum(toSum))
        # set table font
        table = targetDoc.tables[0]
        for rc, row in enumerate(table.rows):
            for cc, cell in enumerate(row.cells):
                for paragraph in cell.paragraphs:
                    if rc == 0 or cc  == 5:
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    elif cc == 0:
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
                    else:
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
                    for run in paragraph.runs:
                        font = run.font
                        font.name = u'標楷體'
                        font.size = Pt(18)
                        run._element.rPr.rFonts.set(
                                qn('w:eastAsia'), u'標楷體')
        # TODO: next page: report details
        targetDoc.add_page_break()
        targetDoc.add_paragraph()
        # new reference document
        filePath = ('./mydocbuilder/monthly_report_detail_template.docx')
        sourceDoc = Document(filePath)
        replaceParagraph = {}
        signatureParagraph = {}
        for paragraph in sourceDoc.paragraphs:
            p = targetDoc.add_paragraph()
            for run in paragraph.runs:
                r = p.add_run(run.text)
                r.font.name = run.font.name
                r.font.size = run.font.size
                r._element.rPr.rFonts.set(qn('w:eastAsia'), u'標楷體')
            p.paragraph_format.alignment = \
                paragraph.paragraph_format.alignment
            if '{' in p.text:
                replaceParagraph['source'] = paragraph
                replaceParagraph['target'] = p
            elif '製表' in p.text:
                signatureParagraph['source'] = paragraph
                signatureParagraph['target'] = p
        # fill in date and such
        d = {}
        day = datetime.date(theYear, theMonth, 1)
        dayE = self.last_day_of_month(day)
        d['ys'], d['ms'], d['ds'] = \
                str(day.year), str(day.month).zfill(2), str(day.day)
        d['ye'], d['me'], d['de'] = \
                str(dayE.year), str(dayE.month).zfill(2), str(dayE.day)
        d['page'] = str(1).zfill(3)
        # reset font
        replaceParagraph.get('target').text = \
                replaceParagraph.get('target').text.format(**d)
        r = replaceParagraph.get('target').runs[0]
        run = replaceParagraph.get('source').runs[0]
        r.font.name = run.font.name
        r.font.size = run.font.size
        r._element.rPr.rFonts.set(qn('w:eastAsia'), u'標楷體')
        #TODO: copy table after replaceParagraph.get('target')
        # save doc
        targetDoc.save('result.docx')

    def last_day_of_month(self, anyday):
        nextMonth = anyday.replace(day=28) + datetime.timedelta(days=4)
        return nextMonth - datetime.timedelta(days=nextMonth.day)

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
