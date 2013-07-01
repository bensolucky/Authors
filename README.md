KDD CUP 2013 - Track 2 - 4th place model
======================================

License
-------
Copyright [2013] [Dmitry Efimov, Lucas Silva, Ben Solecki ] Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Hardware/OS
-----
This was primarily developed on a 32 bit Windows laptop with 4MB RAM. A small number of more memory intensive steps were run on a friend's machine.

3rd Party Software
-----
Python 2.7 with Pandas 10.1

To Run
------
Follow these steps:

1. author_group.py: creates author_groups.csv.  
2. preparse.py:creates Author8a6.tsv and Author2.csv. The former 
3. affiliations.py: generates affs_loose.tsv
4. parse_and_count54.py: run time ~2hrs and generates freq54.csv
5. firstlast54.py - generates the <b>submission file</b> 54.csv