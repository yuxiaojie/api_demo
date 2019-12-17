# api_demo

自动生成 Swagger API 文档


## 运行方式

### 直接启动

```shell

pip3 install -r src/requirements.txt

# 默认端口为 12345
python3 server.py   

# server 启动后，则访问 http://127.0.0.1:12345/api 即可访问在线 api 文档

```

### gunicorn 启动
```shell

pip3 install -r src/requirements.txt

gunicorn -c gun.py server:app

# server 启动后，则访问 http://127.0.0.1:12345/api 即可访问在线 api 文档
```

### docker 启动

```shell

# 本地需要安装并启动 docker 服务

# 未安装 docker-compose 则需要安装
pip3 install docker-compose

docker-compose build 

# 直接启动 
docker-compose up

# 后台启动
docker-compose up -d

```

## 使用范例

### view 实现方式
```python


from app.api.api_base import ApiBlueprint

api = ApiBlueprint('demo')


@api.route('/test', methods=['POST'], summary='v2测试接口',
           params=[api.boxing(PARAM_KEY1, '测试参数1', op_in=api.OP_BODY, require=False, params_type=api.TYPE_INT),
                   api.boxing(PARAM_KEY2, '测试参数2', op_in=api.OP_BODY, params_type=api.TYPE_STRING)],
           resp={'list::列表数据': [{'a::返回数据a': 1, 'b::返回数据b': 2}],
                 'dict::字典数据': {'da::字典数据1': 'da_value', 'db::字典数据2': 2},
                 'val:bool数据:': True},
           errors=[(ERROR_TYPE1_V1, PARAM_KEY1 + ' 格式错误'), (ERROR_TYPE2_V2, '数据异常')])
def demo_test():
    return get_response('modify address success', data={})
```

### view 注册
ApiBlueprint 收集路由信息统一向 flask 注册，在注册路由的同时收集 API 的参数，错误码及响应的数据结构，然后集中存储在内存中，
前端获取 Swagger json 的时候再把收集的数据按 Swagger 语法生成json格式字符串存储在内容中供访问

```python


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
```

### 效果图

![FE90774DC916419A178D23A27F84FDF7](http://cdn.ibeelink.com/FE90774DC916419A178D23A27F84FDF7.png)
