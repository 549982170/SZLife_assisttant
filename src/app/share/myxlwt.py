# coding:utf-8
#!/user/bin/python
'''
Created on 2017年4月26日
@author: yizhiwu
用于绘制
'''
import xlwt
import datetime

ezxf = xlwt.easyxf


def write_xls(file_name, sheet_name, headings, data, heading_xf, data_xfs):
    book = xlwt.Workbook(encoding='utf-8')  # 兼容中文
    sheet = book.add_sheet(sheet_name)
    rowx = 0
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value, heading_xf)
    sheet.set_panes_frozen(True)  # frozenheadings instead of split panes
    sheet.set_horz_split_pos(rowx + 1)  # ingeneral, freeze after last heading row
    sheet.set_remove_splits(True)  # if userdoes unfreeze, don't leave a split there
    for row in data:
        rowx += 1
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value, data_xfs[colx])
    book.save(file_name)


if __name__ == '__main__':
    mkd = datetime.date
    hdngs = ['Date', 'Stock Code', 'Quantity', 'Unit Price', 'Value', 'Message']
    kinds = 'date,text,int,price,money,text'.split(",")  # 需要修改样式的列表
    #数据
    data = [
               [mkd(2007, 7, 1), 'ABC', 1000, 1.234567, 1234.57, ''],
               [mkd(2007, 12, 31), 'XYZ', -100, 4.654321, -465.43, 'Goods returned'],
           ] + [
                   [mkd(2008, 6, 30), 'PQRCD', 100, 2.345678, 234.57, ''],
               ] * 100
    heading_xf = ezxf('font: bold on; align:wrap on, vert centre, horiz center')
    # 对应样式的字典集合
    kind_to_xf_map = {
        'date': ezxf(num_format_str='yyyy-mm-dd'),
        'int': ezxf(num_format_str='#,##0'),
        'money': ezxf('font: italic on;pattern: pattern solid, fore-colour grey25',
                      num_format_str='$#,##0.00'),
        'price': ezxf(num_format_str='#0.000000'),
        'text': ezxf(),
    }
    data_xfs = [kind_to_xf_map[k] for k in kinds]
    write_xls('xlwt_easyxf_simple_demo.xls', 'Demo', hdngs, data, heading_xf, data_xfs)
