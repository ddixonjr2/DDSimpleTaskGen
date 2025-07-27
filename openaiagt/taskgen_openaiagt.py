import asyncio
import messaging_common as msgc
from agents import Agent, Runner, trace, gen_trace_id
from dotenv import load_dotenv
from argparse import ArgumentParser, Namespace

DEFAULT_INSTRUCTIONS = '''
Role: You are a deeply knowledgeable, experienced, 
and encouraging strategic and tactical planner.
Task: You must utilize your vast knowledge of 
how objectives like this have been accomplished,  
determine the most effective strategy, and build a 
realistic set of step in alignment with that strategy.  
Constraints: Avoid profane and disrespectful information.
Avoid all illegal, unethical, and immoral methods and actions.
Eliminate anything rude, unkind, and offensive when 
gathering information and presenting your response.
Input: You will be given a description of the person's objective.
Output: You must organize the response in the form of a bulleted list. 
This list must be broken down in terms of the  milestones, tasks, and 
steps required.  Additionally provide an assessment of the priority of each. 
Use the most encouraging and positive language possible.
Capabilities and Reminders:  You have a vast amount of information at your disposal.  
Remember to use it effectively by focusing on the most proven and highest quality 
guidance available to you.  Also glean as many clues from the request 
to customize the response.
'''
class TaskListGeneratorOAA():
    def __init__(self):
        self.agent = Agent(name=msgc.TASKLIST_GEN_AGENT_NAME)

    async def gen_task_list(self, request: str, instructions: str) -> str:
        self.agent.instructions = instructions
        trace_id = gen_trace_id()
        with trace('Agent API Task List Generator v1', trace_id=trace_id):
            try:
                response = await Runner.run(self.agent, input=request)
                return response.final_output
            except Exception as e:
                header = msgc.AGENT_ERROR_GENERIC_HEADER
                footer = msgc.AGENT_ERROR_GENERIC_FOOTER
                return f'{header}\n{e}\n\n{footer}'
    
async def main():
    load_dotenv()
    generator = TaskListGeneratorOAA()
    parser = ArgumentParser()
    parser.add_argument('--request')
    parser.add_argument('--instructions', default=DEFAULT_INSTRUCTIONS)
    args = parser.parse_args()
    request = args.request or input(f'\n\n{msgc.TASKLIST_GEN_PROMPT} ')
    if request != '':
        instructions = args.instructions or DEFAULT_INSTRUCTIONS
        response = await generator.gen_task_list(request=request, instructions=instructions)
        print(response)
    else:
        print(f'\n{msgc.REQUEST_ERROR_HEADER}')
        print(f'{msgc.REQUEST_ERROR_FOOTER}')

if __name__ == '__main__':
    asyncio.run(main())