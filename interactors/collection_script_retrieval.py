#!/usr/bin/env python

from decorators import *
from icecream import ic
import os

@BashDecorator.decorator
def write_bash_script(content):
  return content

class CollectionScriptRetrievalInteractor:
  __filename = lambda _, x, y: x if y == None else y

  def __init__(self, adapter):
    self.adapter = adapter

  def __get_commands(self, categories):
    commands = []
    for item in categories:
      checkpoints = item.checkpoints
      for checkpoint in range(len(checkpoints)):
        for check in range(checkpoint, checkpoint+1):
          commands.append(checkpoints[checkpoint].checks[check].cmd)
    return ic(commands)

  def execute(self, checklist, output, language):
    categories = self.adapter.checklist_parser(checklist)
    commands = self.__get_commands(categories)
    output = self.__filename(os.path.basename(os.path.splitext(checklist)[0]), output)

    with open(output, 'w') as file:
      if language == "bash":
        content = write_bash_script(commands)
        [file.write(x+'\n') for x in content]
        return 0
      elif language == "batch":
        #TODO
        return 0
      elif language == "powershell":
        #TODO
        return 0
      else:
        return 1
