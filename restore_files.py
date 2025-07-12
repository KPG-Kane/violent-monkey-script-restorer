import os
import re

folderloc_run = os.path.dirname(os.path.abspath(__file__))
folderloc_backups = os.path.join(folderloc_run, "backups")
os.makedirs(folderloc_backups, folderloc_backups)

def main_function():
	for a_folder in os.scandir(folderloc_backups):
		if not a_folder.is_dir(): continue

		# Look inside the folder for the first .log file
		log_file = None
		for entry in os.scandir(a_folder.path):
			if entry.is_file() and entry.name.endswith(".log"):
				log_file = entry.path
				break  # Use the first .log file found

		if (log_file):
			print(f"\nFound log file in '{a_folder.name}'")
			extract_scripts(log_file)
		else:
			print(f"\nNo .log file found in '{a_folder.name}'")

def extract_scripts(log_file):
	# Output folder
	#main_folder = os.path.dirname(log_file)
	main_folder = os.path.basename(os.path.dirname(log_file))
	OUTPUT_FOLDER = os.path.join(folderloc_run, "recovered_scripts", main_folder)
	os.makedirs(OUTPUT_FOLDER, exist_ok=True)

	print(f"Scanning <{log_file}>")
	with open(log_file, "rb") as f:
		data = f.read()

	text = data.decode("utf-8", errors="ignore")

	# Split into lines for easier parsing
	lines = text.split("\n")

	scripts = []
	current_script = []
	collecting = False

	for line in lines:
		strip_line = line.strip()
		
		if "==UserScript==" in strip_line or strip_line.startswith("// ==UserScript=="):
			# Save previous if collecting
			if current_script:
				scripts.append("\n".join(current_script))
			current_script = [line]
			collecting = True
		elif collecting:
			if "==UserScript==" in strip_line:  # New block starts before we saw a clear ending
				scripts.append("\n".join(current_script))
				current_script = [line]
			else:
				current_script.append(line)

	# Catch last one
	if current_script:
		scripts.append("\n".join(current_script))

	print(f"Found {len(scripts)} scripts")

	def sanitise_string(string_in):
		return re.sub(r'[\\/*?:"<>|]', "_", string_in)

	# Save each script to a file
	script_names = []
	for i, script in enumerate(scripts):
		# Try to extract the script name
		
		# Clean up some left over crap...
		script = "// ==UserScript==" + script.split("// ==UserScript==")[1]
		
		# Break up the escaped characters into new lines, etc.
		try:
			# Remove control characters, keep \n and \t
			safe_script = re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', script)
			# Try decoding literal escaped characters like \n, \t, etc.
			script = bytes(safe_script, "utf-8").decode("unicode_escape")
			print("\tUnicode escape decode successful")
		except Exception as e:
			print("\tUnicode escape decoding failed")
			print(e)

		script_lines = script.splitlines()
		
		name = f"script_{i+1}"
		for line in script_lines:
			if line.strip().startswith("// @name"):
				name_candidate = line.strip()[8:].strip()
				if name_candidate:
					name = name_candidate
				break
		if (not name or len(name) < 3): name = f"script_{i+1}"
		
		version = "no-version"
		for line in script_lines:
			if line.strip().startswith("// @version"):
				name_candidate = line.strip()[11:].strip()
				if name_candidate:
					version = name_candidate
				break
		
		# Sanitize filename
		name = sanitise_string(name)
		version = sanitise_string(version)
		filename = f"{name} ({version}).js"
		
		index = 1
		while True:
			if (filename in script_names):
				filename = f"{name} ({version}) ({index}).js"
			else:
				script_names.append(filename)
				break
			index += 1
		
		file_path = os.path.join(OUTPUT_FOLDER, filename)
		
		print(f"\tScript '{filename}' has {len(script_lines)} lines of code")
		
		with open(file_path, "w", encoding="utf-8") as f:
			for line in script_lines:
				f.write(line + '\n')

	print(f"Recovered {len(scripts)} scripts to folder '{os.path.basename(OUTPUT_FOLDER)}'")

main_function()