import asyncio
from taskgenerator import TaskListGenerator
from messaging_common import *
from agents import Agent, Runner, trace, gen_trace_id
from dotenv import load_dotenv
from argparse import ArgumentParser, Namespace

class TaskListGeneratorOAA(TaskListGenerator):
    def __init__(self):
        self.agent = Agent(name=TASKLIST_GEN_AGENT_NAME)

    async def gen_task_list(self, request: str, instructions: str) -> str:
        print(f'Using {self.__class__.__name__} to generate the task list for request:\n{request}')
        self.agent.instructions = instructions
        trace_id = gen_trace_id()
        with trace('Agent API Task List Generator v1', trace_id=trace_id):
            try:
                response = await Runner.run(self.agent, input=request)
                return response.final_output
            except Exception as e:
                header = AGENT_ERROR_GENERIC_HEADER
                footer = AGENT_ERROR_GENERIC_FOOTER
                return f'{header}\n{e}\n\n{footer}'
    
async def main():
    load_dotenv()
    generator = TaskListGeneratorOAA()
    parser = ArgumentParser()
    parser.add_argument('--request')
    parser.add_argument('--instructions', default=DEFAULT_INSTRUCTIONS)
    args = parser.parse_args()
    request = args.request or input(f'\n\n{TASKLIST_GEN_PROMPT} ')
    if request != '':
        instructions = args.instructions or DEFAULT_INSTRUCTIONS
        response = await generator.gen_task_list(request=request, instructions=instructions)
        print(response)
    else:
        print(f'\n{REQUEST_ERROR_HEADER}')
        print(f'{REQUEST_ERROR_FOOTER}')

if __name__ == '__main__':
    asyncio.run(main())