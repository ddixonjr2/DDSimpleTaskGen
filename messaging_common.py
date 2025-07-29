# This file contains the copy constants shared across the application

# Agent Related Constants
TASKLIST_GEN_AGENT_NAME = 'Expert Project Planner and Task List Generator'
TASKLIST_GEN_REQUEST_PREFIX = 'My request is this: In addition to your expertise, please use all the information and tools provided to explain in detail how I could accomplish the following outcome:'
TASKLIST_GEN_CUSTOM_INSTRUCTIONS_PREFIX = 'Please follow these instructions in fulfilling the request stated afterwards:'


AGENT_ERROR_GENERIC_HEADER = 'I could not process your request for the following reason:'
AGENT_ERROR_GENERIC_FOOTER = 'Please resolve the issue and try again.'
REQUEST_ERROR_HEADER = 'Sorry I cannot help without a description of what you would like to accomplish.'
REQUEST_ERROR_FOOTER = 'Please try again by telling me your goal using the "--request" argument or by entering it when prompted.'

# Prompting/Context Related Constants
DEFAULT_ROLE = 'You are a deeply knowledgeable, experienced, and encouraging strategic and tactical planner.'
DEFAULT_TASK = '''You must utilize your vast knowledge of 
how objectives like this have been accomplished,  
determine the most effective strategy, and build a 
realistic set of step in alignment with that strategy.'''
DEFAULT_INPUT = 'You will be given a description of the person\'s objective.'
DEFAULT_OUTPUT = '''You must organize the response in the form of a bulleted list. 
This list must be broken down in terms of the  milestones, tasks, and 
steps required.  Additionally provide an assessment of the priority of each. 
Use the most encouraging and positive language possible.'''
DEFAULT_CONSTRAINTS = '''Avoid profane and disrespectful information.
Avoid all illegal, unethical, and immoral methods and actions.
Eliminate anything rude, unkind, and offensive when 
gathering information and presenting your response.'''
DEFAULT_CAPABILITIES_REMINDERS = '''You have a vast amount of information at your disposal.  
Remember to use it effectively by focusing on the most proven and highest quality 
guidance available to you.  Also glean as many clues from the request 
to customize the response.'''

DEFAULT_INSTRUCTIONS = f'''
Role: {DEFAULT_ROLE}
Task: {DEFAULT_TASK}
Constraints: {DEFAULT_CONSTRAINTS}
Input: {DEFAULT_INPUT}
Output: {DEFAULT_OUTPUT}
Capabilities and Reminders: {DEFAULT_CAPABILITIES_REMINDERS}
'''

# UI Related Constants
TASKLIST_GEN_PROMPT = 'What is your next conquest?'
RESPONSE_INVALID_OBJECTIVE = 'Please enter a valid objective'
RESPONSE_PLACEHOLDER = 'Your task list will appear here'
REQUEST_PLACEHOLDER = 'Describe your end goal here'
DEFAULT_TASKLIST_DIR = 'tasklists'

UI_MAIN_HEADER_TEXT = 'Task List Generator'
UI_TASK_OBJECTIVE_PROMPT = 'What is your next conquest?'
UI_CLEAR_ENTRY_BUTTON_TEXT = 'Clear Entry'
UI_GENERATE_BUTTON_TEXT = 'Generate Task List'
UI_SAVE_BUTTON_TEXT = 'Save Task List'
UI_EXIT_BUTTON_TEXT = 'Done'
TASKLIST_OUTFILENAME_PREFIX = 'tasklist_'