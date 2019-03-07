# api_demo
自动生成 Swagger API 文档

demo:

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

ApiBlueprint 收集路由信息统一向 flask 注册，在注册路由的同时收集 API 的参数，错误码及响应的数据结构，然后集中存储在内存中，
前端获取 Swagger json 的时候再把收集的数据按 Swagger 语法生成json格式字符串存储在内容中供访问


server 启动后，例如在 0.0.0.0:5000 下启动，则访问 http://127.0.0.1:5000/api 即可访问在线 api 文档

![FE90774DC916419A178D23A27F84FDF7](http://cdn.ibeelink.com/FE90774DC916419A178D23A27F84FDF7.png)
