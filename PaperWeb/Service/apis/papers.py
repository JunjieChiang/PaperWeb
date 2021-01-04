from flask_restplus import Resource
from Service.apis import api
from flask import request
from Service.models.papers import PaperModel

class PaperParsers(object):
    @staticmethod               # 静态方法
    def getpaperlist():
        # 解析器
        parser = api.parser()
        parser.add_argument("index", type=int, help="第几页", required=True)       # 自动生成一个text
        parser.add_argument("count", type=int, help="一页包含多少数据", required=True)
        return parser               # 返回解析器

    @staticmethod  # 静态方法
    def getpapersearch():
        # 解析器
        parser = api.parser()
        parser.add_argument("index", type=int, help="第几页", required=True)  # 自动生成一个text
        parser.add_argument("count", type=int, help="一页包含多少数据", required=True)
        parser.add_argument("author", type=str, help="论文作者", required=True)
        return parser  # 返回解析器



class PaperList(Resource):               # 静态方法
    @api.expect(PaperParsers.getpaperlist())        # 将以上解析器运用到此get方法上
    def get(self):
        index = int(request.values.get("index", 0))
        count = int(request.values.get("count", 0))
        papers, has_next = PaperModel.get_paper(index, count)
        return {
            "status": 200,
            "msg": "success",
            "data": papers,
            "index": index,
            "count": count,
            "has_next": has_next
        }


class PaperAuthorSearch(Resource):
    @api.expect(PaperParsers.getpapersearch())  # 将以上解析器运用到此get方法上
    def get(self):
        index = int(request.values.get("index", 0))
        count = int(request.values.get("count", 0))
        author = request.values.get("author", "")
        papers, has_next = PaperModel.get_author_paper(index, count, author)
        return {
            "status": 200,
            "msg": "success",
            "data": papers,
            "index": index,
            "count": count,
            "has_next": has_next
        }


ns = api.namespace("papers", description="论文接口")   # api.namespaces()返回的是list不可作为可迭代器对象因此用api.namespace()
ns.add_resource(PaperList, "", "/")
ns.add_resource(PaperAuthorSearch, "/author", "/author/")
