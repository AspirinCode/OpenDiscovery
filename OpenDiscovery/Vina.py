import sys, os, errno, subprocess
from runProcess import runProcess

def makeFolder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class Vina(object):
	"""Vina driver. Sets up locations of files. """

	def __init__(self, screen, cmpnd, verbose = False):
		self.locations = {}
		self.screen = screen
		self.cmd = runProcess()
		self.cmd.verbose = verbose

		if 'linux' in sys.platform:
			self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-linux/vina"
		elif 'darwin' in sys.platform:
			self.locations['vina'] = screen.protocol_dir + "/OpenDiscovery/lib/vina-osx/vina"

		self.locations['receptor'] = screen.ligand_dir + "/receptor/" + screen.options['receptor'] + ".pdbqt"
		self.locations['ligand'] = screen.ligand_dir + "/ligands/" + cmpnd + ".pdbqt"
		self.locations['config'] = screen.ligand_dir + "/receptor/" + screen.options['receptor'] + ".txt"
		self.locations['results'] = screen.ligand_dir + "/results-"+screen.options['receptor']+"/" + cmpnd + ".pdbqt"
		self.locations['log'] = screen.ligand_dir + "/results-"+screen.options['receptor']+"/" + cmpnd + ".txt"

		makeFolder(screen.ligand_dir + "/results-"+screen.options['receptor'])

	def run(self):
		""" Actually calls the vina binary. """

		self.cmd.run('{vina} --receptor {receptor} --ligand {ligand} --config {conf} --out {results} --log {log} --exhaustiveness {exhaustiveness}'.format(
			vina=self.locations['vina'], receptor=self.locations['receptor'], ligand=self.locations['ligand'],
			conf=self.locations['config'], results=self.locations['results'], log=self.locations['log'],
			exhaustiveness=self.screen.options['exhaustiveness']))