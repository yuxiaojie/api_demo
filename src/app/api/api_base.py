import json
import re
import time
from collections import defaultdict
from app.config import VERSION_STRING
from app.utils.auth_utils import md5

docs = dict()
docs_json = None
path_param_regex = re.compile('<(?:[a-zA-Z0-9]+:)?([a-zA-Z0-9]+)>')


def auto_fill_register(func, params=None, errors=None):
    if not hasattr(func, 'api_params'):
        func.api_params = []
    if not hasattr(func, 'api_errors'):
        func.api_errors = []

    if params:
        func.api_params.extend(params)
    if errors:
        func.api_errors.extend(errors)
    return func


class ApiBlueprint(object):

    # 参数所在位置的枚举
    OP_PATH = 'path'
    OP_QUERY = 'query'
    OP_HEADER = 'header'
    OP_BODY = 'body'

    # 参数类型常量
    TYPE_STRING = 'string'
    TYPE_INT = 'integer'
    TYPE_BOOL = 'boolean'
    TYPE_FLOAT = 'number'
    TYPE_LIST = 'array'
    TYPE_DICT = 'object'

    def __init__(self, name):
        self.name = name
        self.id = md5(str(time.time()))[:6]
        self.deferred = []

    def get_unique(self):
        return self.name + self.id

    @classmethod
    def boxing(cls, key, name, op_in='body', require=True, params_type='string', default=None):
        """
            通过参数生成api文档构造所需要的参数的模型的数据格式
        :param key: 参数的键
        :param name: 参数的描述信息
        :param op_in: 参数所在的部分，取值为path，query，header，body，
        :param require: 该参数是否是必须的，默认为必填
        :param params_type: 参数的类型，默认为string，取值有 integer，string，boolean，number，array，object，注意文件类型也是用string
        :param default: 参数的默认值，默认为None表示不显示默认值项
        :return:
        """
        return {'key': key, 'name': name, 'in': op_in, 'require': require, 'type': params_type, 'default': default}

    def route(self, rule, summary='', params=None, resp=None, errors=None, deprecated=False, **options):
        """
        :param rule: 路径, 注册的接口访问路径
        :param summary: 接口的描述信息, 默认传递空字符串表示接口不写入文档
        :param params: 接口参数声明，默认为None表示不需要参数，
                    传递示例：[{'name': '参数名称', 'in': 'header', 'require': true, 'type': 'string'}, ...]

        :param resp: 接口data域数据声明，数据返回的json格式，在数据的key之后需要以::间隔中文描述，
                    例如： {'name::用户名': 'jeff', 'age::年龄': 17, 'account::用户账号': '1234567', ...}
                    如果是最终值没有键的，可以传递一个tuple，表示第一位是描述，第二位是示例值
                    例如: ('用户名', 'name')

        :param errors: 接口错误声明，默认为None表示接口没有其他错误信息，传递示例：[(error_code, desc), ...]
        :param deprecated: 接口已经废弃的标志
        :param options: flask路由注册的其他参数
        :return:
        """

        if not params:
            params = []
        if not errors:
            errors = []

        methods = options.get('methods', ['GET'])
        doc_rule = path_param_regex.sub('{\g<1>}', rule)

        def wrapper(f):
            self.deferred.append((f, rule, options))

            # 自动注入装饰器需要的参数和错误信息
            if hasattr(f, 'api_params'):
                params.extend(f.api_params)
            if hasattr(f, 'api_errors'):
                errors.extend(f.api_errors)

            # 为防止不同base下有相同的tag，所以文档记录的键使用带随机值的唯一键，保证每个api对象的唯一性
            if self.get_unique() not in docs:
                docs[self.get_unique()] = defaultdict(list)
            for m in methods:
                # 每个http方法都会产生一个文档块
                docs[self.get_unique()][doc_rule].append(
                    {
                        'summary': summary,
                        'params': params,
                        'resp': resp,
                        'errors': errors,
                        'methods': m.lower(),
                        'tags': self.name,
                        'deprecated': deprecated
                    }
                )
            return f
        return wrapper

    def register(self, bp, url_prefix=None):

        # 将路由注册的基础前缀注入文档模型中
        if self.get_unique() in docs:
            for rules in docs[self.get_unique()].values():
                for rule in rules:
                    rule['base'] = bp.name

        if url_prefix is None:
            url_prefix = '/' + self.name

        for f, rule, options in self.deferred:
            endpoint = options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)


def get_docs():

    global docs_json
    if docs_json:
        return docs_json

    # 填充文档的基本信息
    docs_json = {
        'swagger': '2.0',
        'info': {
            'title': 'API文档',
            'description': 'API文档',
            'version': VERSION_STRING
        },
        'host': '127.0.0.1:5000',
        'schemes': [
            'http',
            'https'
        ],
        'produces': [
            'application/json'
        ],
        'consumes': [
            'application/json'
        ]
    }

    tags = set()
    paths = dict()

    for _, all_api in docs.items():
        for url, methods in all_api.items():
            for info in methods:
                if not info['summary']:
                    continue

                tag = info['tags']
                tags.add(tag)
                # 拼接完整的接口url
                curr_url = '/{}/{}{}'.format(info['base'], tag, url)
                if curr_url not in paths:
                    paths[curr_url] = dict()

                # 创建每个接口对应下方法的文档json
                curr_item = {
                    'tags': [tag],
                    'summary': info['summary'],
                    'responses': {
                        '0': {
                            'description': '请求成功',
                            'schema': {
                                'type': 'object',
                                'description': '通用返回格式',
                                'properties': {
                                    'errorCode': {
                                        'type': 'integer',
                                        'description': '请求错误码，0表示成功'
                                    },
                                    'message': {
                                        'type': 'string',
                                        'description': '请求的错误信息'
                                    },
                                    'serverTime': {
                                        'type': 'integer',
                                        'description': '请求的服务器时间'
                                    }
                                }
                            }
                        }
                    }
                }
                paths[curr_url][info['methods']] = curr_item

                if info['params']:
                    curr_item['parameters'] = []
                    body_params = {'in': 'body', 'required': True, 'name': 'body', 'description': '表单数据',
                                   'schema': {'required': [], 'properties': {}}}

                    # body的参数写法不一样，其他的都用同一种格式
                    for param in info['params']:
                        if param['in'] != ApiBlueprint.OP_BODY:
                            curr_item['parameters'].append({
                                'name': param['key'],
                                'description': param['name'],
                                'in': param['in'],
                                'required': param['require'],
                                'type': param['type']
                            })
                        else:
                            if param['require']:
                                body_params['schema']['required'].append(param['key'])
                            body_params['schema']['properties'][param['key']] = {
                                'type': param['type'],
                                'description': param['name']
                            }
                    if body_params['schema']['properties']:
                        curr_item['parameters'].append(body_params)

                if not info['resp']:
                    curr_item['responses']['0']['schema']['properties']['data'] = {
                        'description': '数据域为null'
                    }
                else:
                    curr_item['responses']['0']['schema']['properties']['data'] = resolve_resp_define(info['resp'])

                if info['errors']:
                    for err_code, err_desc in info['errors']:
                        curr_item['responses'][str(err_code)] = {'description': err_desc}

    if paths:
        docs_json['paths'] = paths

    docs_json['tags'] = [{'name': tag} for tag in tags]
    # print(json.dumps(docs_json, indent=4, sort_keys=True, ensure_ascii=False))
    docs_json = json.dumps(docs_json, ensure_ascii=False)
    return docs_json


def get_type(obj):
    if isinstance(obj, list):
        return 'array'
    elif isinstance(obj, str):
        return 'string'
    elif isinstance(obj, float):
        return 'number'
    elif isinstance(obj, bool):
        return 'boolean'
    elif isinstance(obj, int):
        return 'integer'
    else:
        return 'object'


def resolve_resp_define(resp, k=''):
    """
        解析API模型的数据结构生成文档需要的json格式
    :param resp:
    :param k:
    :return:
    """

    # 如果有声明键描述则按规则取出声明的描述
    if k and '::' in k:
        k, desc = k.split("::", 1)
    else:
        desc = ''

    if isinstance(resp, list):
        assert resp
        return {
            'type': 'array',
            'description': '列表数据' if not desc else desc,
            'items': resolve_resp_define(resp[0])
        }
    elif isinstance(resp, dict):
        return {
            'type': 'object',
            'description': '对象数据' if not desc else desc,
            'properties': {sub_k.split("::", 1)[0]: resolve_resp_define(sub_v, sub_k) for sub_k, sub_v in resp.items()}
        }
    elif isinstance(resp, tuple):
        return resolve_resp_define(resp[1], k='::{}'.format(resp[0]))
    else:
        return {
            'type': get_type(resp),
            'description': '返回数据' if not desc else desc
        }
