import discord
import requests
import inspect
import random

class Response:
    def __init__(self, message = None, file: discord.File = None):
        if isinstance(message, discord.File):
            self.file = message
            self.message = None
        else:
	        self.message = message
	        self.file = file

class ErrorMessages:
	@staticmethod
	def _get_calling_command() -> str:
		# Get the name of the function that called the error function
		caller_name = inspect.stack()[2].function
		# Assuming all command handling functions start with 'handle_',
		# strip that prefix to get the command name
		command = caller_name.replace("handle_", "")
		return command

	@staticmethod
	def no_args_needed() -> str:
		command = ErrorMessages._get_calling_command()
		return f"Invalid argument(s) for `***!{command}***` command. Command doesn't take any arguments."

	@staticmethod
	def does_not_take_args() -> str:
		command = ErrorMessages._get_calling_command()
		return f"The `***!{command}***` command doesn't take any arguments."

	@staticmethod
	def arg_count_mismatch() -> str:
		command = ErrorMessages._get_calling_command()
		return f"Invalid number of arguments for `***!{command}***` command. Please provide one or two integers."

	@staticmethod
	def invalid_args_type() -> str:
		command = ErrorMessages._get_calling_command()
		return f"Invalid argument(s) for `***!{command}***` command. Please provide integer values."

	@staticmethod
	def unknown_command(help_command: str = '!help commands') -> str:
		return f"Unknown command. Type `***{help_command}***` to see all the bot commands."

def handle_command(message):
	p_message = message.content.lower()

	# Remove leading and trailing spaces and split the message by spaces for command handling
	parts = p_message.strip().split()
	command = parts[0][1:] # Remove the '!' prefix to get the command name
	args = parts[1:] # The rest of the parts are the arguments

	# Check if the first part starts with the prefix '!'
	if not parts or not parts[0].startswith('!'):
		return None

	if command == "help":
		try:
			if not args:
				print(True)
				return "## ***`!help commands`*** - List all bot commands.\n" \
				       "## ***`!help games`*** - List all bot minigame commands"

		except ValueError:
			return ErrorMessages.does_not_take_args()

	if command == "ping":
		try:
			if len(args) == 0:
				return "Pong!"

			else:
				return ErrorMessages.does_not_take_args()

		except ValueError:
			return ErrorMessages.does_not_take_args()

	elif command == "roll":
		try:
			if len(args) == 1:
				end = int(args[0])
				result = random.randrange(1, end + 1)
				return f'{result}'

			elif len(args) == 2:
				start = int(args[0])
				end = int(args[1])
				if start > end:
					result = random.randrange(end, start + 1)
				else:
					result = random.randrange(start, end + 1)
				return f'{result}'

			else:
				return ErrorMessages.arg_count_mismatch()

		except ValueError:
			return ErrorMessages.invalid_args_type()

	else:
		return ErrorMessages.unknown_command()

def get_response(message) -> Response:
	return Response(handle_command(message))
