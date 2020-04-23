#!/bin/bash

# Set execution permission for linux files. In Colab you should give the permission
# teste
DIR="$1"
chmod +x "$DIR/swat.exe"
chmod +x "$DIR/SUFI2_execute.exe"
chmod +x "$DIR/SWAT_Edit.exe"
chmod +x "$DIR/SUFI2_95ppu.exe"
chmod +x "$DIR/95ppu_NO_Obs.exe"
chmod +x "$DIR/SUFI2_goal_fn.exe"
chmod +x "$DIR/SUFI2_new_pars.exe"
chmod +x "$DIR/SUFI2_95ppu_beh.exe"
chmod +x "$DIR/SUFI2_LH_sample.exe"
chmod +x "$DIR/SUFI2_make_input.exe"
chmod +x "$DIR/SUFI2_extract_hru.exe"
chmod +x "$DIR/SUFI2_extract_rch.exe"
chmod +x "$DIR/SUFI2_extract_sub.exe"
chmod +x "$DIR/extract_hru_No_Obs.exe"
chmod +x "$DIR/extract_rch_No_Obs.exe"
chmod +x "$DIR/extract_sub_No_Obs.exe"
chmod +x "$DIR/extract_hru_Yield_annual_No_Obs_subAvg.exe"

