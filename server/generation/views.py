import json
import os
import random

import lwn_Graphic.combination
import lwn_Graphic.combination2
import lwn_Graphic.constructModel
import lwn_Graphic.constructModel2
import dsp.main

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from server import error_code
from entity.models import Personnel, Item, Scenes
from background.models import ItemPerson


# 全状态
def full_state(request):
    try:
        # pass
        filename = 'fullState.txt'
        os.system('py -2 ' + './efsmGA/GA/ga.py')
        with open('./file/' + filename, 'r', encoding='utf-8') as f:
            results = f.read()
        print(results)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "results": results})
