import logging
import shutil
import stat
import sys
import time
from abc import ABC

import numpy
import pandas as pd
import re
import os
import subprocess
from swatcuppython.moduleinterface import ModuleInterface
from swatcuppython.operationalsystem import OperationalSystem
logger = logging.getLogger(__name__)


class SWATCUP2019(ModuleInterface):
    def __init__(self, operational_system):
        self.operational_system = operational_system
        self.base_path = None

    def get_os_filename(self, linux_file: str, windows_file: str):
        if self.operational_system == OperationalSystem.LINUX:
            return linux_file
        elif self.operational_system == OperationalSystem.WINDOWS:
            return windows_file
        else:
            raise ("Operational system not implemented:" + self.operational_system)

    def set_base_path(self, path):
        self.base_path = path

    def run_os_filename(self, folder_path, filename):
        logger.debug("Running file: " + os.path.join(folder_path, filename))
        process = subprocess.Popen(os.path.join(folder_path, filename), cwd=folder_path)
        # show output
        process.communicate()[0]
        return process.returncode

    def get_version(self) -> str:
        return "SWATCUP2019"

    def windows(self) -> bool:
        return self.operational_system == OperationalSystem.WINDOWS

    def linux(self) -> bool:
        return self.operational_system == OperationalSystem.LINUX

    def sufi2_pre(self, path):
        logger.debug("Running sufi2_pre")
        if self.linux():
            cmd = os.path.join(path, self.get_os_filename("SUFI2_Pre.bat", "SUFI2_Pre.bat"))
            #return subprocess.call(cmd, cwd=path, shell=True)
            process = subprocess.Popen(cmd, shell=True, cwd=path, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE, universal_newlines=True)
            for line in process.stdout:
                sys.stdout.write(line)
            return process.returncode
        if self.windows():
            cmd = os.path.join(path, "SUFI2_Pre.bat")
            #return subprocess.call([cmd], cwd=path, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return subprocess.call([cmd], cwd=path)

    def sufi2_run(self, path):
        logger.debug("Running sufi2_run")
        if self.linux():
            cmd = os.path.join(path, "SUFI2_Run.bat")
            #return subprocess.call(cmd, cwd=path, shell=True)
            #process = subprocess.Popen(cmd, shell=True, cwd=path, stderr=subprocess.STDOUT,
            #                           stdout=subprocess.PIPE, universal_newlines=True)
            #for line in process.stdout:
            #    sys.stdout.write(line)
            #return process.returncode
            process = subprocess.Popen(cmd, shell=True, cwd=path)
            return process.wait()

        if self.windows():
            cmd = os.path.join(path, "SUFI2_Run.bat")
            logger.info('Opening another window, otherwise swat-edit does not work')
            return subprocess.call([cmd], cwd=path, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def sufi2_post(self, path):
        logger.debug("Running sufi2_post")
        if self.linux():
            cmd = os.path.join(path, self.get_os_filename("SUFI2_Post.bat", "SUFI2_Post.bat"))
            #return subprocess.call(cmd, cwd=path, shell=True)
            process = subprocess.Popen(cmd, shell=True, cwd=path, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE, universal_newlines=True)
            for line in process.stdout:
                sys.stdout.write(line)
            return process.returncode
        if self.windows():
            cmd = os.path.join(path, "SUFI2_Post.bat")
            #return subprocess.call([cmd], cwd=path, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return subprocess.call([cmd], cwd=path)

    def sufi2_async_pre(self, path):
        if self.linux():
            cmd = os.path.join(path, self.get_os_filename("SUFI2_Pre.bat", "SUFI2_Pre.bat"))
            return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)
        if self.windows():
            cmd = os.path.join(path, "SUFI2_Pre.bat")
            # se nao criar um NEW CONSOLE o swat_edit da pau em windows. Parece que isso acontece
            # somente dentro do pycharm, se executado diratamente talvez não apresente esse problema
            process = subprocess.Popen([cmd], cwd=path, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       creationflags=subprocess.CREATE_NEW_CONSOLE, universal_newlines=True)
            # Um jeito se colocar Y e S automaticamente. Mas isso não é garantido funcionar em qualquer lingua
            #return process
            # Tenta uma dessas letras para confirma ou não a pergunta sobre continuar
            outs, errs = process.communicate(input=os.linesep.join(["y", "s", "n"]))
            logger.debug("Process out: " + str(outs))
            logger.debug("Process error: " + str(errs))
            # Limpa o diretorio SUFI2.OUT caso tenha dado algum erro com a entrada de Yes,Sim acima
            sufi2_out_folder = os.path.join(path, "SUFI2.OUT")
            filelist = os.listdir(sufi2_out_folder)
            for f in filelist:
                logger.warning("Ooopps, SUFI2.OUT folder is not empty. SUFI2_Pre.bat may not be working! " +
                               "Deleting file: " + os.path.join(sufi2_out_folder, f))
                os.remove(os.path.join(sufi2_out_folder, f))
            return process

    def sufi2_async_run(self, path):
        logger.debug("Runnnig sufi2_async_run")
        if self.linux():
            cmd = os.path.join(path, self.get_os_filename("SUFI2_Run.bat", "SUFI2_Run.bat"))
            return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)
        if self.windows():
            cmd = os.path.join(path, "SUFI2_Run.bat")
            return subprocess.Popen([cmd], cwd=path, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def sufi2_async_post(self, path):
        logger.debug("Running sufi2_async_post")
        if self.linux():
            cmd = os.path.join(path, self.get_os_filename("SUFI2_Post.bat", "SUFI2_Post.bat"))
            return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)
        if self.windows():
            cmd = os.path.join(path, "SUFI2_Post.bat")
            return subprocess.Popen([cmd], cwd=path, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def copy_output(self, project_folder, dst):
        shutil.copytree(os.path.join(project_folder, 'SUFI2.OUT'), dst)

    def set_permissions(self, path):
        """
        Sets proper file permissions for execution under linux. Colab requires that
        :return:
        """
        if self.linux():
            # Execution permission
            logger.debug("Setting files permission for linux")
            os.chmod(os.path.join(path, "swat.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_execute.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SWAT_Edit.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_95ppu.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "95ppu_NO_Obs.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_goal_fn.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_new_pars.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_95ppu_beh.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_LH_sample.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_make_input.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_extract_hru.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_extract_rch.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_extract_sub.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "extract_hru_No_Obs.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "extract_rch_No_Obs.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "extract_sub_No_Obs.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "extract_hru_Yield_annual_No_Obs_subAvg.exe"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_Pre.bat"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_Run.bat"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_Post.bat"), stat.S_IXOTH)
            os.chmod(os.path.join(path, "SUFI2_extract.bat"), stat.S_IXOTH)





    def sufi2_lh_sample(self, path):
        logger.debug("Running SUFI2_LH_sample")
        self.run_os_filename(path, self.get_os_filename("SUFI2_LH_sample.exe", "SUFI2_LH_sample.exe"))

    def sufi2_execute(self, path):
        logger.debug("Running SUFI2_execute")
        self.run_os_filename(path, self.get_os_filename("SUFI2_execute.exe", "SUFI2_execute.exe"))

    def sufi2_goal_fn(self, path):
        logger.debug("Running SUFI2_goal_fn")
        self.run_os_filename(path, self.get_os_filename("SUFI2_goal_fn.exe", "SUFI2_goal_fn.exe"))

    def sufi2_new_pars(self, path):
        logger.debug("Running SUFI2_new_pars")
        self.run_os_filename(path, self.get_os_filename("SUFI2_new_pars.exe", "SUFI2_new_pars.exe"))

    def sufi2_95ppu(self, path):
        logger.debug("Running SUFI2sufi2_95ppu")
        self.run_os_filename(path, self.get_os_filename("SUFI2_95ppu.exe", "SUFI2_95ppu.exe"))

    def sufi2_95ppu_beh(self, path):
        logger.debug("Running SUFI2_95ppu_beh")
        self.run_os_filename(path, self.get_os_filename("SUFI2_95ppu_beh.exe", "SUFI2_95ppu_beh.exe"))

    def read_sufi2_out_goal(self, path: str):
        file = "/media/jairo/Dados/Jairo/Projetos/SWAT/git/SWATPython/sufi2.Sufi2.SwatCup/SUFI2.OUT/goal.txt"
        fo = open(file, "r")
        # Le informacoes das primeiras linhas
        line1 = re.findall(r"[^\s\,!?;'\"]+", fo.readline())
        line2 = re.findall(r"[^\s\,!?;'\"]+", fo.readline())
        line3 = re.findall(r"[^\s\,!?;'\"]+", fo.readline())

        if line1[0] == "no_pars=":
            param_number = int(line1[1])
        else:
            raise ValueError("Invalid goal file:" + file)

        if line2[0] == "no_Sims=":
            simulation_number = int(line2[1])
        else:
            raise ValueError("Invalid goal file:" + file)

        if line3[0] == "type_of_goal_fn=":
            goal_type = line3[1]
        else:
            raise ValueError("Invalid goal file:" + file)

        info = {"no_pars": param_number,
                "no_sims": simulation_number,
                "type_of_goal_fn": goal_type}

        print(info)
        # Le informações da tabela
        # data_widths = [5] + [9] * param_count
        df = pd.read_csv(fo, header=0, delim_whitespace=True)
        print(df)

