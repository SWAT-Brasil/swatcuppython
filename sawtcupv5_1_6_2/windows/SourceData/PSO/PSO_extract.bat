@echo off
:: required
make_trk.exe
::
PSO_extract_rch.exe
rem PSO_extract_hru.exe
rem PSO_extract_sub.exe
::
rem extract_rch_No_Obs.exe
rem extract_hru_No_Obs.exe
rem extract_sub_No_Obs.exe






::
::
::
::
:: Remarks:
::
:: The trk.exe program keeps trak of the number of simulations
:: Then, extrcat files are run as necessary to extrcat variables
:: from rch, hru, and sub output files as required to formulate the
:: objective function.
::
:: Variables for which there are no observation could also be extracted
:: from rch, hru, and sub output files.
::