
import re

from app.api.api_response import get_response
from app.api.constants import PARAM_KEY1, PARAM_KEY2, ERROR_TYPE1_V1, ERROR_TYPE2_V2
from app.api.api_base import ApiBlueprint

BASE_LOC_PATTERN = re.compile(r'(\d+)\.(\d+)(?:\.\d+)?;')


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
