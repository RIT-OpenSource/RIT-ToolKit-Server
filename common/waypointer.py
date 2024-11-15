from json import loads, dumps
from os.path import exists, abspath
from os import mkdir

from .logger import lyLogger


class Waypointer():
    json_file_path = './data/waypoint/list.json'
    # 获得 Logger 操作器
    logger = lyLogger('log/', 'server.log', 'Waypointer')
    #
    def __init__(self):
        if not exists('./data'): mkdir('data')
        if not exists('./data/waypoint'): mkdir('./data/waypoint')
        if not exists(self.json_file_path):
            with open(self.json_file_path, 'w', encoding='utf-8') as ListFile:
                ListFile.write(dumps(
                    [
                        {
                            'name': '\u57fa\u5730',
                            'x': -172,
                            'y': 102,
                            'z': 321,
                            'Dim': 'Overworld',
                            'ID': 'LingyunAwA',
                            'wid': 1
                        }
                    ]
                ))
        else:
            with open(self.json_file_path, 'r', encoding='utf-8') as ListFile:
                fc = ListFile.read()
            if fc == None or fc == '':
                with open(self.json_file_path, 'w', encoding='utf-8') as ListFile:
                    ListFile.write(dumps(
                        [
                            {
                                'name': '\u57fa\u5730',
                                'x': -172,
                                'y': 102,
                                'z': 321,
                                'Dim': 'Overworld',
                                'ID': 'LingyunAwA',
                                'wid': 1
                            }
                        ]
                    ))
        self.logger.log('初始化路径管理器')
    #
    def getall(self):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as ListFile:
                data = loads(ListFile.read())
                self.logger.log('获取全部数据 | 成功')
                return data
        except:
            self.logger.warn('获取全部数据 | 未找到文件')
            return {}
    #
    def get(self, name):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as ListFile:
                List = loads(ListFile.read())
        except:
            self.logger.error('获取指定数据 | 错误：未找到文件')
            raise FileNotFoundError(f'Missing Data File: {abspath(self.json_file_path)} is not exists.')
        for counter in List:
            if counter['name'] == name:
                self.logger.log('获取指定数据 | 成功')
                return [counter['value'], counter['id']]
        self.logger.warn('获取全部数据 | 未找到数据')
        return None
    #
    def join(self, name, x, y, z, dim, id):
        wid = _Helper().genWID()
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as ListFile:
                List:list = loads(ListFile.read())
            List.append({
                'name': name,
                'x': x,
                'y': y,
                'z': z,
                'dim': dim,
                'ID': id,
                'wid': wid
            })
            with open(self.json_file_path, 'w', encoding='utf-8') as ListFile:
                ListFile.write(dumps(List))
            _Helper().addWID()
            self.logger.log('加入指定数据 | 成功')
        except BaseException as ex:
            self.logger.error(f'加入指定数据 | 失败，错误为：\n    {ex}')
    #
    def remove(self, name):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as ListFile:
                List = loads(ListFile.read())
            updated_list = [counter for counter in List if counter['wid'] != int(name)]
            with open(self.json_file_path, 'w', encoding='utf-8') as ListFile:
                ListFile.write(dumps(updated_list))
            _Helper().minusWID()
            self.logger.log('删除指定数据 | 成功')
        except BaseException as ex:
            self.logger.error(f'删除指定数据 | 失败，错误为：\n    {ex}')

class _Helper():
    num_file_path = './data/waypoint/num.txt'
    def addWID(self):
        with open(self.num_file_path, 'r', encoding='utf-8') as NumFile:
            num = int(NumFile.read())
        num += 1
        with open(self.num_file_path, 'w', encoding='utf-8') as NumFile:
            NumFile.write(str(num))
    #
    def genWID(self):
        with open(self.num_file_path, 'r', encoding='utf-8') as NumFile:
            num = int(NumFile.read())
        num += 1
        return num
    #
    def minusWID(self):
        with open(self.num_file_path, 'r', encoding='utf-8') as NumFile:
            num = int(NumFile.read())
        num -= 1
        with open(self.num_file_path, 'w', encoding='utf-8') as NumFile:
            NumFile.write(str(num))