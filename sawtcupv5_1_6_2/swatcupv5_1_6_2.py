import logging
from abc import ABC

import numpy
import pandas as pd
import re
import os
import subprocess
from swatcuppython.moduleinterface import ModuleInterface
from swatcuppython.operationalsystem import OperationalSystem
logger = logging.getLogger(__name__)


class SWATCUPv5_1_6_2(ModuleInterface):
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
        return "SWAT-CUPv5.1.6.2"

    def sufi2_pre(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Pre.bat", "SUFI2_Pre.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        subprocess.call(cmd, cwd=path, shell=True)

    def sufi2_run(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Run.bat", "SUFI2_Run.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        subprocess.call(cmd, cwd=path, shell=True)

    def sufi2_post(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Post.bat", "SUFI2_Post.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        subprocess.call(cmd, cwd=path, shell=True)

    def sufi2_async_pre(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Pre.bat", "SUFI2_Pre.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)

    def sufi2_async_run(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Run.bat", "SUFI2_Run.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)

    def sufi2_async_post(self, path):
        cmd = os.path.join(path, self.get_os_filename("SUFI2_Post.bat", "SUFI2_Post.bat"))
        logger.debug(cmd)
        # TODO: shell=True eh um falaha de seguranca. Mas o bat so funciona assim. Corrigir no futuro
        return subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.DEVNULL)

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

