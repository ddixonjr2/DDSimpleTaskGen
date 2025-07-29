import asyncio
import langchain_core.messages as lcm
import langchain_openai as lcoa
from messaging_common import *

from taskgenerator import TaskListGenerator
from requestargparse import TaskListGen_ArgParser
from dotenv import load_dotenv

class TaskListGeneratorLC(TaskListGenerator):
    def __init__(self):
        self.llm = lcoa.ChatOpenAI()

    async def gen_task_list(self, request: str, instructions: str) -> str:
        print(f'Using {self.__class__.__name__} to generate the task list for request:\n{request}')
        try:
            sys_message = lcm.SystemMessage(instructions)
            user_message = lcm.HumanMessage(request)
            messages = [sys_message, user_message]
            response = self.llm.invoke(messages)
            return response.content if response else f'{AGENT_ERROR_GENERIC_HEADER}\nNo response from LLM.\n{AGENT_ERROR_GENERIC_FOOTER}'
        except Exception as e:
            return f'{AGENT_ERROR_GENERIC_HEADER}\n{e}\n{AGENT_ERROR_GENERIC_FOOTER}'

async def main():
    load_dotenv()
    generator = TaskListGeneratorLC()
    request_parser = TaskListGen_ArgParser()
    request = request_parser.request or input(f'{UI_TASK_OBJECTIVE_PROMPT} ')
    instructions = request_parser.instructions
    
    if request and request != '':
        print('Working on your task list...')
        response = await generator.gen_task_list(request=request, instructions=instructions)
        print(f'\n\n{response}')
    else:
        response = f'\n{REQUEST_ERROR_HEADER}\n{REQUEST_ERROR_FOOTER}'
        print(response)
        
if __name__ == '__main__':
    asyncio.run(main())