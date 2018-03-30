# coding:utf-8
#!/user/bin/python
'''
Created on 2017年2月10日
@author: yizhiwu
系统配置全局变量,添加需要缓存的新表建立,再添加加载配置库sql
'''
import collections
import logging
from app.db.dbentrust.dbpool import dbpool
logger = logging.getLogger('dblog')

# ------------默认Id为主键的配置缓存表-------------------
tb_syscfg = collections.OrderedDict()  # 系统配置表


# ------------需要缓存的新表结束-------------------
def load_admin_data():
    """从数据库中读取配置信息加载到内存 """

    def load_data(sql_, dict_, index_str='Id'):
        """执行加载语句
        @param sql_:
        @param dict_:
        """
        res = dbpool.querySql(sql_, True)
        dict_.clear()
        for item in res:
            dict_[long(item[index_str])] = item

    logger.info('加载数据配置数据开始 ...')
    # ----------------加载配置库-----------------
    sql = "SELECT * FROM tb_syscfg order by Id"
    load_data(sql, tb_syscfg)  # 系统配置

    # ----------------加载配置库结束---------------
    logger.info('加载数据配置数据完毕 ...')


def get_syscfg_val(syscfg_id):
    """
    通过系统配置表的id获取值
    @param syscfg_id:
    @return:
    """
    ret = tb_syscfg.get(int(syscfg_id))
    if ret is None:
        raise Exception('not syscfg id=%s' % syscfg_id)
    return str(ret['content'])


def get_sequence_val(seq_name):
    """
    获取sequence表中序列的下一个值
    @param seq_name: 表名
    """
    try:
        sql = "select nextval_safe('%s')" % seq_name
        conn = dbpool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
    except Exception, err:
        conn.rollback()
        logger.error('sqlerror: %s ' % sql)
        raise err
    finally:
        cursor.close()
        conn.close()
    return result[0]
