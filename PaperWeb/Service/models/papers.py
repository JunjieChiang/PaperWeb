from Service.libs.mysql import db                   # 导入数据库

class PaperModel(object):
    @staticmethod                            # 静态方法: 不用实例化类，直接使用类名PaperModel去调用方法
    def get_paper(index, count):
        # 获得数据库papers列表
        sql = f'''
            SELECT
                id,
                title,
                url
            FROM
                papers
            WHERE
                is_deleted=0
            LIMIT {(index-1) * count}, {count+1}
        '''

        result = db.query(sql)
        if not result:
            return [], 0                    # 如果是null,返回空,没有下一页
        if len(result) == count + 1:
            result.pop()
            has_next = 1                    # 是否有下一页
        else:
            has_next = 0
        return result, has_next

    @staticmethod
    def get_author_paper(index, count, author):
        '''获取某个作者写的所有论文的id,title,url'''
        author = db.escape_string(author)                   # 转码:防止有特殊字符

        sql = f"""
            SELECT
                id,
                title,
                url
            FROM
                papers
            WHERE
                authors LIKE "%{author}%"
                AND is_deleted = 0
            LIMIT {(index - 1) * count}, {count + 1}                # 限制
        """

        result = db.query(sql)
        if not result:
            return [], 0                        # 如果是null,返回空,没有下一页
        if len(result) == count + 1:
            result.pop()
            has_next = 1                        # 是否有下一页
        else:
            has_next = 0
        return result, has_next