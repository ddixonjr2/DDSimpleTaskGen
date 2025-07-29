from taskgenerator import TaskListGenerator
from taskgen_openaiagt import TaskListGeneratorOAA
from taskgen_langchain import TaskListGeneratorLC
from taskgen_crewai import TaskListGeneratorCA
from enum import Enum

# Engine
# An enum to represent the choices of implement ways to get the same outcome. 
# `Engine` was the best non-conflicting name I could conjure for now to represent
# a combination of framework/approach to deriving the same result. :)
# As a learning method and evolution of the code, my plan is to add several more 
# engines such as those that use frameworks like CrewAI and protocols 
# like MCP--all selectable thorough the UI.
class Engine(Enum):
    LANGCHAIN = 'LangChain API'
    OPENAIAGT = 'OpenAI Agent API'
    CREWAI = 'CrewAI API'

class TaskListGeneratorSelector():
    def __init__(self):
        self.generator = None

    def generator_matches(self, engine: Engine) -> bool:
        if self.generator is None or not isinstance(self.generator, TaskListGenerator):
            return False
        else: 
            return  (engine == Engine.OPENAIAGT and isinstance(self.generator, TaskListGeneratorOAA)) or \
                    (engine == Engine.LANGCHAIN and isinstance(self.generator, TaskListGeneratorLC)) or \
                    (engine == Engine.CREWAI and isinstance(self.generator, TaskListGeneratorCA))

    def cur_task_list_generator(self, engine: Engine) -> TaskListGenerator:
        if self.generator_matches(engine):
            return self.generator
        else:
            self.generator = self.new_tasklist_generator(engine)
            return self.generator

    def new_tasklist_generator(self, engine: Engine) -> TaskListGenerator:
        generator = None
        match engine:
            case Engine.OPENAIAGT:
                generator = TaskListGeneratorOAA()
            case Engine.LANGCHAIN:
                generator = TaskListGeneratorLC()
            case Engine.CREWAI:
                generator = TaskListGeneratorCA()
            case _:
                generator = TaskListGeneratorOAA()
                
        return generator
