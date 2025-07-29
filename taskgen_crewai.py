import asyncio
from messaging_common import *

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from taskgenerator import TaskListGenerator
from dotenv import load_dotenv
from requestargparse import TaskListGen_ArgParser

class TaskListGeneratorCA(TaskListGenerator):
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7
        )
        self.agent = Agent(
            role=DEFAULT_ROLE,
            goal=f'{DEFAULT_INPUT} {DEFAULT_OUTPUT}',
            backstory=f'{DEFAULT_CAPABILITIES_REMINDERS} {DEFAULT_CONSTRAINTS}',
            llm=self.llm
        )

    # Note that in the case of CrewAI, the components of the content found
    # in the all-inclusive instructions text is already passed into
    # the instance of Agent. This does however allow for separate instructions
    # to be passed in.
    async def gen_task_list(self, request, instructions):
        print(f'Using {self.__class__.__name__} to generate the task list for request:\n{request}')
        default_description = f'{TASKLIST_GEN_REQUEST_PREFIX} {request}'
        custom_description = f'{TASKLIST_GEN_CUSTOM_INSTRUCTIONS_PREFIX}\n{default_description}'
        has_no_custom_instructions = instructions is None or instructions == ''
        generation_description = default_description if has_no_custom_instructions else custom_description
        
        task = Task(
            name=TASKLIST_GEN_AGENT_NAME,
            description=generation_description,
            agent=self.agent,
            expected_output=DEFAULT_OUTPUT
        )
        crew = Crew(
            agents=[self.agent],
            tasks=[task]
        )
        
        response = await crew.kickoff_async()
        return response 

async def main():
    load_dotenv()
    generator = TaskListGeneratorCA()
    request_parser = TaskListGen_ArgParser()
    request = request_parser.request or input(f'{UI_TASK_OBJECTIVE_PROMPT} ')
    instructions = request_parser.instructions

    if request and request != '':
        print(UI_INPROGRESS_TEXT)
        response = await generator.gen_task_list(request=request, instructions=instructions)
        print(f'\n\n{response}')
    else:
        response = f'\n{REQUEST_ERROR_HEADER}\n{REQUEST_ERROR_FOOTER}'
        print(response)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
