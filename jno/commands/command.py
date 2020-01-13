from jno.util import get_all_models
from jno.util import formatted_help_string
from jno.util import JnoException
from colorama import Fore
from sys import version_info


class Command():

	help_name = "Command"
	help_usage = "None"
	help_description = "None"

	def __init__(self,argv,location=None):
		if argv and argv[-1] == "help":
			print(formatted_help_string(self,surround=True))
			return
		self.run(argv,location)


	# Overload this function in actual commands
	def run(self,argv,location):
		pass


	# Return proper board formatting
	def formatBoard(self,board_input,jno_dict):
		prepared_board_string = None
		model = None
		board = None
		param_list = []
		value_list = []
		# get all supported models
		all_models = get_all_models(jno_dict)
		
		# parse board string to separate board from possible paramters
		if ":" in board_input:
			# get board name separate from param_string
			try:
				board,param_string = board_input.split(":")
			except ValueError:
				raise JnoException("invalid board input; there should be max of 1 ':'")
			else:
				# get param and value pairs from raw string
				params_raw = param_string.split(",")
				for param_raw in params_raw:
					try:
						param,value = param_raw.split("=")
					except ValueError:
						raise JnoException("invalid board input; each parameter can only have 1 '='")
					else:
						param_list.append(param)
						value_list.append(value)
		# otherwise, the board name should havbe been provided
		else:
			board = board_input

		# get model
		for some_model in all_models:
			if some_model.board == board:
				model = some_model
				break
		# if not found, raise exception
		if model is None:
			raise JnoException("board '{}' not recognized".format(board))

		# figure out which params were provided; if not provided, choose default val
		if version_info < (3,0): # python2 code
			for param_type,data in model.menu_item_dict.iteritems():
				self.fill_out_param_value_lists(param_list,value_list,param_type,data)
		else: # python3 code
			for param_type,data in model.menu_item_dict.items():
				self.fill_out_param_value_lists(param_list,value_list,param_type,data)

		# if there are parameters to be input, account for that
		if len(param_list) > 0:
			prepared_board_string = model.get_prefix() + model.board + ":"
			string_params = []
			# combine param and value for strings
			for param,value in zip(param_list,value_list):
				string_params.append("{0}={1}".format(param,value))
				print("Setting {} to {}".format(param,value))
			prepared_board_string += ','.join(string_params)
		# otherwise, don't do anything with it
		else:
			prepared_board_string = model.get_prefix() + model.board
		# return prepared string
		return prepared_board_string

	# Helper function for formatBoard function
	def fill_out_param_value_lists(self,param_list,value_list,param_type,data):
		# if this param type doesn't have choices, skip it
		if data.is_empty():
			return
		# if this param was provided by the user, skip it
		if param_type in param_list:
			return
		# otherwise, choose default value for it
		param_list.append(param_type)
		value_list.append(data.get_first().name)
