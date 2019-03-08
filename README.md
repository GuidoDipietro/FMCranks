# FMCranks
Raw text input to nicely formatted XLSX file
------------------------------------------------------------------------------------------

#### Requisites: Python 2 or 3, Excel, xlsxwriter and excel2img (installed via .bat file)

## How it works:
1. 	### Copy as plain text every comment from the "RESULTS:" section of the post.
	If you want to see how it should look like, just open the file FMCranks.txt as it is now.
	You'd want to delete everything before you paste the new data, of course.

	#### *NOTE*:
	If any competitor didn't include a "=" sign in their comment, add it manually. It can be anywhere in the line.
	- Example:
		- Guido Dipietro 20,23,21 World Record!
	- Change to:
		- Guido Dipietro 20,23,21 World Record!=
	
	That should be okay
	#### Data needed in each competitor line to function properly:
	- Full name + Result1 + Result2 + Result3 + "=" sign
	- Only the name and the 6 digits comprising the 3 results are taken into account.
	- Every other character is ignored, such as commas, periods, etc.

2.	### Run "runme.bat"
	#### *IMPORTANT*:
	edit it and change the path to the folder you're at.
	It will do your work and write the results neatly to the file "FMCranks.xlsx"
	(library xlsxwriter is downloaded by this file, if you don't have it)

3. 	### Open the file "FMCranks.xlsx" for the Excel or "FMCranks.bmp" for the image.
	Enjoy!

Any questions PM me to my FB (Guido Dipietro) or email dipietroguido@gmail.com
If it fails at any point please do contact me.
