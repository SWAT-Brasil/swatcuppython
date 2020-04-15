@echo off
:: required
make_trk.exe
::
rem MCMC_extract_rch.exe
rem copy model_rch.out   model.out
::
rem MCMC_extract_hru.exe
rem copy model_hru.out   model.out
rem copy model_rch.out+model_hru.out  model.out
::
rem MCMC_extract_sub.exe
rem copy model_sub.out   model.out
rem copy model_rch.out+model_sub.out  model.out
rem copy model_hru.out+model_sub.out  model.out
rem copy model_rch.out+model_hru.out+model_sub.out  model.out
::
rem extract_rch_No_Obs.exe
rem extract_hru_No_Obs.exe
rem extract_sub_No_Obs.exe




:: Remarks
::
:: Variables can be extrcated from rch,hru,and sub output files
:: to formulate an objective function. They need to be copied 
:: to model.out
:: If the objective function contains variables from both
:: rch and hru files, then they must be appended together
:: in the model.out file. So, depending on the extrcated varibales 
:: and the structure of the objective function, the approperiate 
:: copy command above must be checked.
:: 

