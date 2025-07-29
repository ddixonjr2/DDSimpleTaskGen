# An abstract class to define required interface for task generators

from abc import ABC, abstractmethod

class TaskListGenerator(ABC):
    @abstractmethod
    async def gen_task_list(self, request: str, instructions: str) -> str:
        pass
