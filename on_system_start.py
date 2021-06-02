import sys  # to find autostart in arguments
# from appdirs import user_data_dir
# from configparser import ConfigParser
# import os



def start_on_boot_enabled():
	if '--autostart' in sys.argv:
		return True
	return False
	# config_file = "config.ini"
	# config_file_path = user_data_dir()
	# print("from on_system_start file: ", os.path.join(config_file_path, config_file))

	# if os.path.exists(os.path.join(config_file_path, config_file)):
	# 	config = ConfigParser()
	# 	config.read(os.path.join(config_file_path, config_file))

	# 	saved_start_at = int(config['default']['start_at'])
	# 	if saved_start_at == 1:
	# 		print("from on_system_start file: ", saved_start_at)
	# 		print("Auto start")
	# 		return True
	return False