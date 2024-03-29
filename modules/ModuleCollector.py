import importlib
import sys

class ModuleCollector:
	def __init__(self):
		self._modules = {}

	def add(self, name):
		if name in self._modules: raise KeyError("Module already loaded")
		spec = importlib.util.find_spec(name)
		if not spec: raise ImportError(f"Failed to load {name}")
		lib = importlib.util.module_from_spec(spec)
		sys.modules[name] = lib
		self._modules[name] = lib
		try:
			spec.loader.exec_module(lib)
		except:
			self._modules.pop(name)
			del sys.module[name]
			raise ImportError("Failed to load module")

	def remove(self, name):
		if name not in self._modules: raise KeyError("Module not loaded")
		self._modules.pop(name)
		del sys.module[name]

	def get(self, name):
		if name not in self._modules: raise KeyError("Module does not exist")
		return self._modules[name]

	def reload(self, name):
		self.remove(name)
		self.add(name)
