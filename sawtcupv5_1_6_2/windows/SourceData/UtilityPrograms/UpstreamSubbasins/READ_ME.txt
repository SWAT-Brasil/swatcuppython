Upstream_subbasins_sorted.exe
--------------------------------------

This program finds all the upstream subbasin for a given outlet


input:
    upstream.def
    upstream_from_to.txt   .......  this file is from the SWAT database. 
                                    Open project's .mdb file --> Reach --> copy the column 'from' and 'to'
                                    into this text file


output:
    upstream_sorted.out
    upstream.out




subtract_subbasins.exe
---------------------------------------

This program subtracts common subbasins from two given lists of upstream subbasins for two outlets(usually taken from upstream_sorted.out)

input:
  subtract.txt       
  outlet_no=   8880  4627		In this file, in the given example  
						the first number is the subbasin (outlet)number,
						and the second number is the number of subbasins in the upstream of that outlet

output:
  subtract.out              this file has the list of excess subbasins
   
  



