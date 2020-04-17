@echo off
:: required
GLUE_trk.exe
::
GLUE_extract_rch.exe
copy model_rch.out   model.out
::
rem GLUE_extract_hru.exe
rem copy model_hru.out   model.out
rem copy model_rch.out+model_hru.out  model.out
::
rem GLUE_extract_sub.exe
rem copy model_sub.out   model.out
rem copy model_rch.out+model_sub.out  model.out
rem copy model_hru.out+model_sub.out  model.out
rem copy model_rch.out+model_hru.out+model_sub.out  model.out
::
rem extract_hru_No_Obs.exe
rem extract_rch_No_Obs.exe
rem extract_sub_No_Obs.exe


::
::
::
::
:: Remarks:
::
:: Variables can be extrcated from rch, hru, and sub output files to formulate an objective function.
:: The simulated outputs need to be copied to model.out file.
:: If the objective function contains variables from output.rch file alone, then these outputs are simply
:: copied to model.out. If outputs come from both rch and hru files, then they must be appended together
:: in the model.out using the DOS command: copy model_rch.out+model_hru.out  model.out
::
:: So, depending on the extrcated varibales and the structure of the objective function, the approperiate
:: copy command above must be checked.
::::