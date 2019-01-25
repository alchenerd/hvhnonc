# -*- coding: utf-8 -*-
"""
@author: alchenerd (alchenerd@gmail.com)
"""
import sqlite3
from copy import copy, deepcopy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
import os
import comtypes.client
import datetime
import sys
import xlwt
import deprecation

wdFormatPDF = 17

if __name__ == '__main__': # at mydocbuilder
    sys.path.append('../')

from myconnect import connect

class DocBuilder():
    """DocBuilder is a customized docx creator exclusively for hvhnonc."""
    def __init__(self, type_: str = 'default', **kwargs):
        self.actions = {
                'default': self.hello_docx,
                'register_list': self.create_register_list,
                'unregister_list': self.create_unregister_list,
                'monthly_report': self.create_monthly_report,
                'full_report': self.create_full_report}
        if self.actions.get(type_, None):
            self.type_ = type_
        else:
            self.type_ = 'default'
            self.kwargs.clear()
        self.kwargs = kwargs.get('kwargs')

    def set_type(self, type_: str = 'default'):
        """Sets the which type of the document to build."""
        self.type_ = type_

    def set_kwargs(self, **kwargs):
        """Sets the form info into the doc builder."""
        self.kwargs = deepcopy(kwargs)

    def construct(self):
        """Constructs a docx and save it."""
        # see self.actions for individual construct functions
        self.actions[self.type_]()

    def hello_docx(self):
        """Makes a dummy hello docx document."""
        document = Document()
        document.add_heading('Hello .docx!', 0)
        p = document.add_paragraph('This is my test paragraph!')
        records = ((2, 9, 4), (7, 5, 3), (6, 1, 8))
        table = document.add_table(rows=0, cols=3)
        for x, y, z in records:
            rowCells = table.add_row().cells
            rowCells[0].text = str(x)
            rowCells[1].text = str(y)
            rowCells[2].text = str(z)
        document.save('result.docx')

    @deprecation.deprecated()
    def full_report(self):
        """Opens full report template, then modify and save it."""
        print('full_report')
        ref = Document('./mydocbuilder/full_report_template.docx')
        doc = Document('./mydocbuilder/full_report_template.docx')
        # fetch data
        rows = self.get_remain_items()
        dataCount = sum(1 for i in rows)
        # populate pages
        ROW_PER_PAGE = 12
        pageNeeded = dataCount // ROW_PER_PAGE \
                      + (dataCount % ROW_PER_PAGE > 0)
        # replace last line with empty string
        p = doc.paragraphs[-1]
        p.text = ''
        # insert pages
        for i in range(1, pageNeeded):  # page 0 is in template
            # page break
            doc.add_page_break()
            p = doc.add_paragraph()
            # copy table
            table = ref.tables[0]
            tbl = table._tbl
            new_tbl = deepcopy(tbl)
            p._p.addnext(new_tbl)
        # add last line with font in reference
        p = doc.add_paragraph(ref.paragraphs[-1].text)
        r = p.runs[0]
        r.font.name = u'標楷體'
        r.font.size = Pt(16)
        r._element.rPr.rFonts.set(qn('w:eastAsia'), u'標楷體')
        # write data to table
        for i, row in enumerate(rows):
            tableIndex = i // ROW_PER_PAGE
            rowIndex = i % ROW_PER_PAGE + 1  # skip title row
            cells = doc.tables[tableIndex].rows[rowIndex].cells
            # cells[0]: outlist id(date + page)
            tmp = row['acquire_date'].split('-')
            ymstring = ''.join(tmp[:-1])
            tmp = ymstring + str(row['page']).zfill(2)
            cells[0].text = tmp
            # cells[1]: objid + serial
            cells[1].text = ' - '.join(map(str, (row['object_ID'],
                                                 row['serial_ID'])))
            # cells[2]: name
            cells[2].text = row['name']
            # cells[3]: spec
            cells[3].text = row['spec']
            # cells[4]: unit
            cells[4].text = row['unit']
            # cells[5]: amount
            cells[5].text = str(row['amount'])
            # cells[6]: price
            cells[6].text = str(row['price'])
            # cells[7]: total price
            cells[7].text = str(row['price'] * row['amount'])
            # cells[8]: acquire date
            cells[8].text = str(row['acquire_date']).replace('-', '/')
            # cells[9]: keep_year
            cells[9].text = str(row['keep_year'])
            # cells[10]: place
            cells[10].text = row['place']
            # cells[11]: keep_department
            cells[11].text = row['keep_department']
            # cells[12]: keeper
            cells[12].text = row['keeper']
        # set data texts to small font(Pt 10)
        for table in doc.tables:
            for row_i, row in enumerate(table.rows):
                if row_i == 0:  # skip title row
                    continue
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(10)
        # save file
        doc.save('result.docx')
        # convert to excel
        self.docx_tables_to_excel()
        # convert to PDF
        cwd = os.getcwd()
        self.docx_to_pdf(cwd + '\\\\result.docx', cwd + '\\\\result.pdf')

    def get_remain_items(self):
        """Get the hvhnonc_in exclude hvhnonc_out items in a list."""
        con, cur = connect._get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # fetch ID and amount only
        # conditions and params from self.kwargs
        d = {'conditions': ''}
        params = []
        for k, v in self.kwargs.items():
            if 'date' in k:
                # date string tuple, skip acquire_date
                if k == 'acquire_date':
                    continue
                d['conditions'] += '({} between ? and ?) and '.format(k)
                params.extend(v)
            else:
                d['conditions'] += ('{} like ? and '.format(k))
                params.append(v)
        # hvhnonc_in
        sqlstr = (
                'select id, amount '
                'from hvhnonc_in '
                'where {conditions}1')
        cur.execute(sqlstr.format(**d), params)
        rows = cur.fetchall()
        inData = {row['id']: row['amount'] for row in rows}
        print('IN:', len(inData), 'rows.')
        # hvhnonc_out, all unregister records
        sqlstr = (
                'select hvhnonc_out.in_id as id, hvhnonc_out.amount '
                'from hvhnonc_out '
                'inner join hvhnonc_in '
                'on hvhnonc_in.id = hvhnonc_out.in_id')
        cur.execute(sqlstr)
        rows = cur.fetchall()
        outData = {row['id']: row['amount'] for row in rows}
        print('OUT:', len(outData), 'rows.')
        # data substraction
        result = deepcopy(inData)
        for id, amt in outData.items():
            if result.get(id, None):
                result[id] -= amt
                if result[id] == 0:
                    result.pop(id)
                elif result[id] < 0:
                    print('delisted too much: {0}'.format((id)))
                    result.pop(id)
        # fetch detail of the remainders
        for i, (id, amount) in enumerate(result.items()):
            sqlstr = (
                    'select page, object_id, serial_id, name, spec, unit, '
                    'price, acquire_date, keep_year, place, '
                    'keep_department, keeper from hvhnonc_in where id = ?')
            params = (str(id),)
            cur.execute(sqlstr, params)
            row = deepcopy(dict(cur.fetchone()))
            row['amount'] = amount
            yield row
        con.close()
        return

    def setMyFont(self, doc):
        """Set normal font of doc as my font."""
        doc.styles['Normal'].font.name = u'標楷體'
        doc.styles['Normal'].font.size = Pt(12)
        doc.styles['Normal']._element.rPr.rFonts.set(
                qn('w:eastAsia'), u'標楷體')

    @deprecation.deprecated()
    def monthly_report(self):
        """Opens monthly report template, then modify and save it."""
        print('monthly_report')
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
        # next page: report details
        # fetch the in and out record within the month
        records = self.construct_record_rows(theYear, theMonth)
        # calculate the page needed
        ROW_PER_PAGE = 17
        pageNeeded = len(records) // ROW_PER_PAGE \
                   + (len(records) % ROW_PER_PAGE > 0)
        print('appending', pageNeeded, 'pages.')
        # dictionary for replacement
        d = {}
        day = datetime.date(theYear, theMonth, 1)
        dayE = self.last_day_of_month(day)
        d['ys'], d['ms'], d['ds'] = \
                str(day.year), str(day.month).zfill(2), str(day.day)
        d['ye'], d['me'], d['de'] = \
                str(dayE.year), str(dayE.month).zfill(2), str(dayE.day)
        # construct pages
        refPath = ('./mydocbuilder/monthly_report_detail_template.docx')
        refDoc = Document(refPath)
        for pg in range(pageNeeded):
            targetDoc.add_page_break()
            for paragraph in refDoc.paragraphs:
                if '{' in paragraph.text:
                    d['page'] = str(pg + 1).zfill(3)
                    tempText = paragraph.text.format(**d)
                    p = targetDoc.add_paragraph(tempText)
                    # copy table
                    table = refDoc.tables[0]
                    tbl = table._tbl
                    new_tbl = deepcopy(tbl)
                    p._p.addnext(new_tbl)
                elif pg != pageNeeded - 1 and '製表' in paragraph.text:
                    continue
                else:
                    p = targetDoc.add_paragraph(paragraph.text)
                for r in p.runs:
                    run = paragraph.runs[0]
                    r.font.name = run.font.name
                    r.font.size = run.font.size
                    r._element.rPr.rFonts.set(qn('w:eastAsia'), u'標楷體')
                p.paragraph_format.alignment = \
                    paragraph.paragraph_format.alignment
        for i, record in enumerate(records):
            # fetch table and row count
            tableCount = i // ROW_PER_PAGE
            rowCount = i % ROW_PER_PAGE
            # get table and row
            table = targetDoc.tables[tableCount + 1] # 0 is used in summary
            row = table.rows[rowCount + 2] # 0 and 1 are title rows
            for j, column in enumerate(record):
                r = row.cells[j].paragraphs[0].add_run(column)
                r.font.name = u'標楷體'
                r.font.size = Pt(12)
                r._element.rPr.rFonts.set(qn('w:eastAsia'), u'標楷體')
        # save file
        targetDoc.save('result.docx')
        # convert tables to excel
        self.docx_tables_to_excel()
        # convert to PDF
        cwd = os.getcwd()
        self.docx_to_pdf(cwd + '\\\\result.docx', cwd + '\\\\result.pdf')

    def construct_record_rows(self, y, m):
        first_day_of_month = datetime.date(y, m, 1)
        last_day_of_month = self.last_day_of_month(first_day_of_month)
        records = []
        con, cur = connect._get_connection()
        con.set_trace_callback(print)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        #con.set_trace_callback(print)
        # fetch all categories
        cur.execute('select description from hvhnonc_category')
        rows = cur.fetchall()
        categories = []
        for row in rows:
            for column in row:
                categories.append(column)
        # fill in data for each category
        totalRow = [u'總計', '', '', '', '', '0', '', '0', '', '', '']
        for category in categories:
            # fetch from db
            # select register data
            # conditions from the form
            d = {'conditions': ''}
            params = []
            for k, v in self.kwargs.items():
                if 'date' in k:
                    # date string tuple, skip acquire date
                    if k == 'acquire_date':
                        continue
                    d['conditions'] += '({} between ? and ?) and '.format(k)
                    params.extend(v)
                else:
                    d['conditions'] += ('{} like ? and '.format(k))
                    params.append(v)
            selIn = (
                    'select '
                        '"i" as type_, name, brand, spec, unit, price, '
                        'amount, acquire_date as date, place, remark '
                    'from '
                        'hvhnonc_in '
                    'where '
                        'category = :category '
                        'and {conditions}1 '
                        'and acquire_date '
                            'between :first_day_of_month '
                            'and :last_day_of_month ')
            selIn = selIn.format(**d)
            # select unregister data
            selOut = (
                    'select '
                        '"o" as type_, i.name as name, i.brand as brand, '
                        'i.spec as spec, i.unit as unit, i.price as price, '
                        'o.amount as amount, o.unregister_date as date, '
                        'o.unregister_place as place, '
                        'o.unregister_remark as remark '
                    'from '
                        'hvhnonc_out as o '
                    'inner join '
                        'hvhnonc_in as i '
                    'on '
                        '(o.in_id = i.id) '
                        'and {conditions}1 '
                        'and i.category = :category '
                        'and o.unregister_date '
                            'between :first_day_of_month '
                            'and :last_day_of_month ')
            selOut = selOut.format(**d)
            # what we want is union all order by date
            print('__SELIN__: ' + selIn)
            print('__SELOUT__: ' + selOut)
            params = params + params
            sqlstr = (selIn + 'union all ' + selOut + 'order by date asc')
            # dictionary
            params = {
                    'category': category,
                    'first_day_of_month': str(first_day_of_month),
                    'last_day_of_month': str(last_day_of_month)}
            cur.execute(sqlstr, params)
            rows = cur.fetchall()
            titleRow = [category, '', '', '', '', '', '', '', '', '', '']
            subtotalRow = [u'小計', '', '', '', '', '0', '', '0', '', '', '']
            if len(rows):
                # 1st row: category as title
                records.append(titleRow)
                # parse the row
                for row in rows:
                    dataRow = []
                    dataRow.append(row['name'])
                    desc = ' '.join((row['brand'], row['spec']))
                    dataRow.append(desc)
                    dataRow.append(row['unit'])
                    dataRow.append(str(row['price']))
                    if row['type_'] == 'i':
                        tp = row['amount'] * row['price']
                        dataRow.append(str(row['amount']))
                        dataRow.append(str(tp))
                        dataRow.append('')
                        dataRow.append('')
                        subtotalRow[5] = str(int(subtotalRow[5]) + tp)
                        totalRow[5] = str(int(totalRow[5]) + tp)
                    elif row['type_'] == 'o':
                        tp = row['amount'] * row['price']
                        dataRow.append('')
                        dataRow.append('')
                        dataRow.append(str(row['amount']))
                        dataRow.append(str(tp))
                        totalRow[5] = str(int(totalRow[5]) + tp)
                    else:
                        dataRow.append('')
                        dataRow.append('')
                        dataRow.append('')
                        dataRow.append('')
                    datestr = row['date'].split('-')
                    datestr[0] = str(int(datestr[0]) - 1911)  # ROC years
                    datestr = '-'.join(datestr)
                    dataRow.append(datestr)
                    dataRow.append(row['place'])
                    dataRow.append(row['remark'])
                    records.append(copy(dataRow))
                records.append(subtotalRow)
        records.append(totalRow)
        con.close()
        return records

    def get_todays_ROC_date_str(self):
        """Returns today's month string in ROC date e.g. 1010101"""
        today = datetime.date.today()
        thestr = [str(today.year - 1911), str(today.month).zfill(2)]
        return ''.join(thestr)

    def last_day_of_month(self, anyday):
        """Return the last day of month of a given day."""
        nextMonth = anyday.replace(day=28) + datetime.timedelta(days=4)
        return nextMonth - datetime.timedelta(days=nextMonth.day)

    @deprecation.deprecated()
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
                mstr = self.get_todays_ROC_date_str()
                replacements['srl'] = mstr + '-01'
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
        ROW_PER_PAGE = 7
        pageCount = rowCount // ROW_PER_PAGE + (rowCount % ROW_PER_PAGE > 0)
        print(rowCount, 'rows, ', pageCount, 'pages.')
        # page copying
        for i in range(1, pageCount): # from page 2 to pageCount
            # serial(dynamically changes each page)
            mstr = self.get_todays_ROC_date_str()
            replacements['srl'] = mstr + '-'
            replacements['srl'] += str(i + 1).zfill(2)
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
            # using the (i // ROW_PER_PAGE * 2)th table
            tableIndex = i // ROW_PER_PAGE * 2
            table = targetDoc.tables[tableIndex]
            # using the (i % ROW_PER_PAGE + 1)th row (1st row is title)
            rowIndex = i % ROW_PER_PAGE + 1
            try:
                tableRow = table.rows[rowIndex]
                for j, c in enumerate(tableRow.cells):
                    print('[{0}]:{1}'.format(j, rowList[j]), end='')
                    c.text = str(rowList[j])
                    strwidth = self.count_string_width(c.text)
                    # width to fontsize
                    if strwidth >= 24:
                        fontsize = 8
                    elif strwidth >= 20:
                        fontsize = 9
                    elif strwidth >= 16:
                        fontsize = 10
                    elif strwidth >= 13:
                        fontsize = 11
                    else:
                        fontsize = 12
                    for p in c.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(fontsize)
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
        # save file
        targetDoc.save('result.docx')
        # convert to excel
        self.docx_tables_to_excel()
        # convert to PDF
        cwd = os.getcwd()
        self.docx_to_pdf(cwd + '\\\\result.docx', cwd + '\\\\result.pdf')

    def count_string_width(self, s):
        """Count the width of a string, w=1 for ascii, w=2 for others."""
        return sum([1 if 0 <= ord(x) and ord(x) <= 127 else 2 for x in s])

    def rows_to_excel(self, rows):
        """Save sqlite3.Rows rows to result.excel."""
        assert all([isinstance(row, sqlite3.Row) for row in rows]), 'bad rows'
        wb = xlwt.Workbook()
        ws = wb.add_sheet('result')
        titles = list(rows[0].keys())
        # write in titles
        for i, title in enumerate(titles):
            ws.write(r=0, c=i, label=title)
        # write in values
        for rc, row in enumerate(rows):
            for tc, title in enumerate(titles):
                try:
                    tmp = str(row[title])
                except Exception:
                    # pass if something went wrong
                    continue
                ws.write(r=(rc + 1), c=tc, label=tmp)
        wb.save('result.xls')

    def docx_tables_to_excel(self):
        """For some doc, it is faster to just read tables from docx."""
        docx = Document('result.docx')
        wb = xlwt.Workbook()
        ws = wb.add_sheet('result')
        xlsrow = 0
        for table in docx.tables:
            for row in table.rows:
                for cc, cell in enumerate(row.cells):
                    ws.write(xlsrow, cc, cell.text)
                xlsrow += 1
            xlsrow += 1
        wb.save('result.xls')

    @deprecation.deprecated()
    def register_list(self):
        """Opens a copy of add template, then modify and save it."""
        print('register_list')
        # get the month
        edmin, edmax = self.kwargs.get('acquire_date', (None, None))
        if edmin:
            theYear, theMonth = edmin.year, edmin.month
        elif edmax:
            theYear, theMonth = edmax.year, edmax.month
        else:
            today = datetime.datetime.today()
            theYear, theMonth = today.year, today.month
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
                # srl = date(ROC) + page
                mstr = self.get_todays_ROC_date_str()
                replacements['srl'] = mstr
                replacements['srl'] += '-01'
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
                    'acquire_date, keep_year, place, keep_department, '
                    'keeper, id '
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
        ROW_PER_PAGE = 7
        pageCount = rowCount // ROW_PER_PAGE + (rowCount % ROW_PER_PAGE > 0)
        print(rowCount, 'rows, ', pageCount, 'pages.')
        # page copying
        for i in range(1, pageCount): # from page 2 to pageCount
            # serial(year(ROC), month, page)
            mstr = self.get_todays_ROC_date_str()
            replacements['srl'] = mstr + '-'
            replacements['srl'] += str(i + 1).zfill(2)
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
            # at (i // ROW_PER_PAGE + 1)th page
            pageIndex = i // ROW_PER_PAGE + 1
            # update column `page` in hvhnonc_in
            con, cur = connect._get_connection()
            cur.execute('update hvhnonc_in set page = ? where id = ?',
                        (pageIndex, row['id']))
            # using the (i // ROW_PER_PAGE * 2)th table
            tableIndex = i // ROW_PER_PAGE * 2
            table = targetDoc.tables[tableIndex]
            # using the (i % ROW_PER_PAGE + 1)th row (1st row is title)
            rowIndex = i % ROW_PER_PAGE + 1
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
            con.commit()
            print()
            print('page:', pageIndex,
                  ', table:', tableIndex,
                  ', row:', rowIndex, ' done!')
        con.close()
        # save file
        targetDoc.save('result.docx')
        # convert to excel
        self.docx_tables_to_excel()
        # convert to PDF
        cwd = os.getcwd()
        self.docx_to_pdf(cwd + '\\\\result.docx', cwd + '\\\\result.pdf')

    def docx_to_pdf(self, in_file, out_file):
        word = comtypes.client.CreateObject('Word.Application')
        docx = word.Documents.Open(in_file)
        docx.SaveAs(out_file, FileFormat=wdFormatPDF)
        docx.Close()
        word.Quit()

    def create_register_list(self):
        """Creates a register list, saves data as excel, docx, and pdf."""

        def fetch_from_database(d):
            """Returns a list of sqlite3.Row as data"""
            print(d)
            con, cur = connect._get_connection(useSQL3Row=True)
            con.set_trace_callback(print)
            sqlstr = ('select {columns} from {table} where {conditions}')
            replacements = {}
            # columns: object_ID, serial_ID, name, spec, unit, amount, price,
            #          acquire_date, keep_year, keep_department, place, keeper
            replacements['columns'] = ', '.join((
                    'object_ID', 'serial_ID', 'name', 'spec', 'unit', 'amount',
                    'price', 'acquire_date', 'keep_year', 'keep_department',
                    'place', 'keeper'))
            # table: hvhnonc_in
            replacements['table'] = 'hvhnonc_in'
            # conditions: determined by d
            replacements['conditions'] = ''
            params = []
            for k, v in d.items():
                if 'date' in k:
                    # date string tuple
                    replacements['conditions'] += \
                            '({} between ? and ?) and '.format(k)
                    params.extend(v)
                else:
                    replacements['conditions'] += \
                            ('{0} like ? and '.format(k))
                    params.append('%' + v + '%')
            replacements['conditions'] += '1'
            # fill in the blanks
            sqlstr = sqlstr.format(**replacements)
            cur.execute(sqlstr, params)
            data = cur.fetchall()
            con.close()
            for row in data:
                print(', '.join([str(row[k]) for k in row.keys()]))
            return data

        def parse_for_document(rows):
            """Parse sqlite3 rows to list of list for document table uses."""
            if len(rows) == 0:
                return [[]]
            result = []
            colTitle = ['物品編號', '物品名稱', '規格', '單位', '數量', '單價',
                        '總價', '取得日期', '使用年限', '存置地點',
                        '保管或使用單位', '保管或使用人']
            result.append(colTitle)
            # data
            for row in rows:
                # result row
                rrow = []
                # rrow[0]: objid + serial
                obj_ID = row['object_ID'].replace(' ', '')
                s = '-'.join((obj_ID, row['serial_ID']))
                rrow.append(s)
                # rrow[1:6]: name, spec, unit, amount, price
                rrow.append(str(row['name']))
                rrow.append(str(row['spec']))
                rrow.append(str(row['unit']))
                rrow.append(str(row['amount']))
                rrow.append(str(row['price']))
                # rrow[6]: total price
                rrow.append(str(row['amount'] * row['price']))
                # rrow[7]: acquire_date(EE/mm/dd)
                date = list(map(int, row['acquire_date'].split('-')))
                date[0] = date[0] - 1911
                date = list(map(lambda x: str(x).zfill(2), date))
                rrow.append('/'.join(date))
                # rrow[8:12]: keep_year, keep_department, place, keeper
                rrow.append(str(row['keep_year']))
                rrow.append(str(row['place']))
                rrow.append(str(row['keep_department']))
                rrow.append(str(row['keeper']))
                result.append(rrow)
            print(result)
            return result

        def write_to_excel(arr, fn):
            """Save 2d list to result.excel."""
            wb = xlwt.Workbook()
            ws = wb.add_sheet('result')
            for rc, row in enumerate(arr):
                for cc, column in enumerate(row):
                    try:
                        ws.write(r=rc, c=cc, label=column)
                    except:
                        # skip if encounter problems
                        continue
            wb.save(fn)

        def construct_docx(data):
            """Open template, then modify according to rowCount."""
            doc = Document('./mydocbuilder/register_list_template.docx')
            # set font to 標楷體(16)
            self.setMyFont(doc)
            # fill in the header
            header = doc.sections[0].header
            replaceRow = header.tables[0].rows[0]
            # fill in department
            target_paragraph = replaceRow.cells[0].paragraphs[0]
            target_paragraph.text = \
                    target_paragraph.text.format(**{'dept': '秘書室'})
            target_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            # fill in the date
            target_paragraph = replaceRow.cells[1].paragraphs[0]
            today = datetime.date.today()
            s = [str(today.year - 1911), str(today.month).zfill(2),
                 str(today.day).zfill(2)]
            s = '中華民國{0}年{1}月{2}日'.format(*s)
            target_paragraph.text = s
            target_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            for i, datum in enumerate(data[1:]):
                row = doc.tables[0].add_row()
                for cc, cell in enumerate(row.cells):
                    cell.paragraphs[0].text = datum[cc]
                print('row', i, '/', len(data) - 1, 'appended!')
            return doc

        # indicate entry
        print('create_register_list')
        # fetch data from database
        data = fetch_from_database(self.kwargs)
        # parse data for xls, docx
        data = parse_for_document(data)
        # write data and save to excel
        write_to_excel(data, 'result.xls')
        # write to docx template
        document = construct_docx(data)
        # save .docx
        document.save('result.docx')
        """
        # convert to pdf and save (using current working directory)
        cwd = os.getcwd()
        self.docx_to_pdf(cwd + '\\\\result.docx', cwd + '\\\\result.pdf')
        """

    def create_unregister_list(self):
        # TODO:  finish this method
        pass

    def create_monthly_report(self):
        # TODO:  finish this method
        pass

    def create_full_report(self):
        # TODO:  finish this method
        pass

def main():
    myDocBuilder = DocBuilder()
    myDocBuilder.construct()


if __name__ == '__main__':
    main()
