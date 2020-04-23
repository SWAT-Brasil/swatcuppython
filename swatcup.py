import os
import logging
import subprocess
import shutil
import subprocess
import platform
from swatcuppython.swatcupversion import SWATCUPVersion
from swatcuppython.operationalsystem import OperationalSystem
from swatcuppython.sawtcupv5_1_6_2.swatcupv5_1_6_2 import SWATCUPv5_1_6_2
from swatcuppython.swatcup2019.swatcup2019 import SWATCUP2019

logger = logging.getLogger(__name__)


class SWATCUP(object):
    """
    Swat is a python interface for SWAT. It is based in modules, so each SWAT version has a different
    module. Using modules allows the interface to be used with different swat versions.

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self, version):
        """ Initialize SWAT class. Use SWAT.SWATVersion and SWAT.OS enuns.

        Parameters
        ----------
        version : SWATVersion enun
            SWAT version to use
        operational_system : OS enun
            Operational System (WINDOWS or LINUX)
        """
        self.version = version
        self.operational_system = platform.system()
        self.architecture = platform.architecture()[0]
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.project_folder_path = None
        self.executable_path = None
        self.wrapper = None
        self.executable_filename = None
        self.swatcuppython_base_folder_name = "swatcuppython"
        self.swatcuppython_base_folder_path = None
        self.process_number = 1;
        self.async_process = None

        logger.info("Detected OS: " + self.operational_system + " " + self.architecture)
        # Select the right class for the swat version
        if version == SWATCUPVersion.SWATCUPv5_1_6_2:
            if self.operational_system == OperationalSystem.LINUX.value:
                self.wrapper = SWATCUPv5_1_6_2(OperationalSystem.LINUX)
            elif self.operational_system == OperationalSystem.WINDOWS.value:
                self.wrapper = SWATCUPv5_1_6_2(OperationalSystem.WINDOWS)

        if version == SWATCUPVersion.SWATCUP2019:
            if self.operational_system == OperationalSystem.LINUX.value:
                self.wrapper = SWATCUP2019(OperationalSystem.LINUX)
            elif self.operational_system == OperationalSystem.WINDOWS.value:
                self.wrapper = SWATCUP2019(OperationalSystem.WINDOWS)


        logger.info("Using SWATCUPPython module: " + self.wrapper.get_version())

    def __del__(self):
        # Kills any async task that might be running
        self.sufi2_run_async_kill();

    def set_project_folder(self, path):
        """ Set the project folder

        Parameters
        ----------
        path : path to folder that should be already created
        """
        if not os.path.isdir(path):
            logger.error("Project folder nof found: " + path)
            raise ValueError("Project folder not found: " + path)
        self.project_folder_path = path
        logger.info("Project folder found: " + path)
        self.wrapper.set_permissions(path)
        # Cria diretorio de operacao swatcuppython se ainda não existe
        self.swatcuppython_base_folder_path = os.path.join(self.project_folder_path,
                                                           self.swatcuppython_base_folder_name)
        if not os.path.isdir(self.swatcuppython_base_folder_path):
            logger.info("Creating swatcuppython folder: " + self.swatcuppython_base_folder_path)
            os.mkdir(self.swatcuppython_base_folder_path)
        else:
            logger.info("Found swatcuppython folder: " + self.swatcuppython_base_folder_path)

    def sufi2_pre(self):
        self.wrapper.sufi2_pre(self.project_folder_path)

    def sufi2_run(self):
        self.wrapper.sufi2_run(self.project_folder_path)

    def sufi2_async_pre(self):
        if self.sufi2_async_is_running():
            raise ValueError("SUFI2 is already running")
        else:
            self.async_process = self.wrapper.sufi2_async_pre(self.project_folder_path)

    def sufi2_async_run(self):
        if self.sufi2_async_is_running():
            raise ValueError("SUFI2 is already running")
        else:
            self.async_process = self.wrapper.sufi2_async_run(self.project_folder_path)

    def sufi2_async_post(self):
        if self.sufi2_async_is_running():
            raise ValueError("SUFI2 is already running")
        else:
            self.async_process = self.wrapper.sufi2_async_post(self.project_folder_path)

    def sufi2_run_async_kill(self):
        if self.sufi2_async_is_running():
            logger.debug("Found a running SUFI2 process running. Killing it!")
            self.async_process.kill()

    def sufi2_async_is_running(self) -> bool:
        if self.async_process is None:
            return False
        elif self.async_process.poll() is None:
            return True
        else:
            return False

    def sufi2_async_return_code(self) -> int:
        return self.async_process.poll()

    def sufi2_async_wait(self):
        logger.debug("Waiting SUFI2")
        self.async_process.wait()


    def sufi2_post(self):
        self.wrapper.sufi2_post(self.project_folder_path)

    def read_sufi2_out_goal(self):
        self.wrapper.read_sufi2_out_goal(os.path.join(self.project_folder_path), "/SUFI2.OUT/goal.txt")

    ################ Rotinas utilizadas no processamento paralelo - ainda não funciona #################
    # def sufi2_pre(self, process: int):
    #   self.wrapper.sufi2_pre(self.get_process_folder_path(process))

    # def sufi2_run(self, process: int):
    #   self.wrapper.sufi2_run(self.get_process_folder_path(process))

    # def sufi2_pos(self, process: int):
    #   self.wrapper.sufi2_post(self.get_process_folder_path(process))

    # def load_backup(self):
    #   self.load_backup()

    # def sync_files(self, source_path, dest_path):
    #    if self.operational_system == OperationalSystem.LINUX.value:
    #        logger.debug("Syncing files: '" + source_path + "' -> '" + dest_path + "'")
    #        cmd = "rsync " + source_path + "/* " + dest_path
    #        subprocess.call(cmd, shell=True)
    #        #TODO Criar diretorios antes do sync em caso de vazio
#
#        elif self.operational_system == OperationalSystem.WINDOWS.value:
#            logger.error("Windows sync file not implemented")
#        else:
#            logger.error("Unknown operational system:" + self.operational_system)

#    def set_process_number(self, number):
#        self.process_number = number

#    def sync_processes(self):
#        for i in range(self.process_number):
#            self.sync_process(i)

#    def get_process_folder_path(self, process: int):
#        if isinstance(process, int):
#            if 0 <= process < self.process_number:
#                return os.path.join(self.swatcuppython_base_folder_path, "process" + str(process))
#            else:
#                raise ValueError("Process out of range: (0: " + str(self.process_number-1) + ")")
#        else:
#            raise ValueError("Process should be an Int type")


#    def sync_process(self, process: int):
#        if isinstance(process, int):
#            if 0 <= process < self.process_number:
#                logger.debug("Sync process :" + str(process))
#                process_folder = os.path.join(self.swatcuppython_base_folder_path, "process" + str(process))
#                self.sync_files(self.project_folder_path, process_folder)
#                self.sync_files(os.path.join(self.project_folder_path, "SUFI2.IN"),
#                                os.path.join(process_folder, "SUFI2.IN"))
#                self.sync_files(os.path.join(self.project_folder_path, "SUFI2.OUT"),
#                                os.path.join(process_folder, "SUFI2.OUT"))
#                self.sync_files(os.path.join(self.project_folder_path, "Echo"),
#                                os.path.join(process_folder, "Echo"))
#                self.sync_files(os.path.join(self.project_folder_path, "Backup"),
#                                os.path.join(process_folder, "Backup"))


#            else:
##                raise ValueError("Process out of range: (0: " + str(self.process_number-1) + ")")
#        else:
#            raise ValueError("Process should be an Int type")


#    @staticmethod
#    def run_os_filename(folder_path, command):
#        logger.debug("Running file: " + command)
#        process = subprocess.Popen(["rsync", "-vt", "/media/jairo/Dados/Jairo/Projetos/SWAT/git/SWATPython/my_swatcup_project/Backup", "/media/jairo/Dados/Jairo/Projetos/SWAT/git/SWATPython/my_swatcup_project/swatcuppython/process3"])
#        # show output
#        process.communicate()[0]
#        return process.returncode
