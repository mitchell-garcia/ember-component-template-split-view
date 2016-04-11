import sublime, sublime_plugin, logging

class EmberComponentSplitViewCommand(sublime_plugin.WindowCommand):

	# @public findCompanionPodStructure
	# @return {String} newFile - the file to open
	def findCompanionPodStructure(self):
		if 'hbs' in self.reference_file_type:
			companion_file = self.reference_file_path + '/component.js'
		else:
			companion_file = self.reference_file_path + '/template.hbs'

		return companion_file

	# @public findCompanionFolderStucture
	# @return {String} newFile - the file to open 
	def findCompanionFolderStucture(self):
		base_path = self.reference_file_path.rsplit('/app/', 1)[0] + '/app/'

		if 'hbs' in self.reference_file_type:
			companion_file_name = self.reference_file_name.rsplit('.', 1)[0] + '.js'
			companion_file = base_path + 'components/' + self.reference_file_location + '/' + companion_file_name
		else:
			companion_file_name = self.reference_file_name.rsplit('.', 1)[0] + '.hbs'
			companion_file = base_path + 'templates/' + self.reference_file_location + '/' + companion_file_name

		return companion_file

	def checkIfUsePods(self):
		settings = sublime.load_settings('EmberComponentSplitView.sublime-settings')
		use_pods_defined = settings.has('usePods')
	
		if(use_pods_defined):
			return settings.get('usePods')

		return 'pods' in self.reference_file_location

	# @public findFile
	# @return {String} fileToOpen
	def processFile(self):
		self.reference_file = self.window.active_view().file_name()
		self.reference_file_path = self.reference_file.rsplit('/', 1)[0]
		self.reference_file_name = self.reference_file.rsplit('/', 1)[1]
		self.reference_file_type = self.reference_file.rsplit('.', 1)[-1]
		self.reference_file_location = self.reference_file_path.rsplit('/app/', 1)[1]

		usePods = self.checkIfUsePods()

		if usePods:
			companion_file = self.findCompanionPodStructure()
		else:
			companion_file = self.findCompanionFolderStucture()

		return companion_file

	def run(self):
		file = self.processFile()

		self.window.focus_group(0)
		self.window.open_file(self.window.active_view().file_name())

		self.window.focus_group(1)
		self.window.open_file(file)
