#!/usr/bin/env python

import hjson
import json
from models import *

class ChecklistAdapter():
  def checklist_parser(filename):
    with open(filename, 'r') as hjson_file:
      hson_checklist = hjson.loads(hjson_file.read())
      json_checklist = hjson.dumpsJSON(hson_checklist)
      checklist = json.loads(json_checklist)

    categories_list = []
    for item in checklist:
      categories_list = []
      for category in item['categories']:
        checkpoints_list = []
        for checkpoint in category['checkpoints']:
          checks_list = []
          for check in checkpoint['checks']:
            checks_list.append(Check(**check))
          checkpoint['checks'] = checks_list
          checkpoints_list.append(Checkpoint(**checkpoint))
        category['checkpoints'] = checkpoints_list
        categories_list.append(Category(**category))

    return categories_list
