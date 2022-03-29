# RGB_OCR
Guide to RGB and OCR Programmes
Getting started
Have Python downloaded and use an appropriate viewer, e.g. PyCharm or Jupyter Notebook.
Download the source code from github:
Download tesseract, e.g. from: https://pypi.org/project/tesseract-ocr/#files
Upon download completion, input letsgodigital files from programme into tessdata file of tesseract.
   
RGB
The RGB is relatively straightforward to install and use.
Insert parameters (lines 10-18):
  
Should be self-explanatory although note:
•	Directory (line 11): input directory name where photos are located. Do not include any files which are not to be analysed.
•	Paths should be inputted as r’path_name’. Removing the r will cause the programme to break.
•	Region_limits (lines 13-15): up to three (pri, sec, ter) desired regions for RGB mean. These are most easily chosen by putting show_first_pic as “Y” or “Yes” and entering the x and y values of the top left and bottom right corners of your desired rectangle (found bottom right, e.g. 668 and 908 below). Rectangle colours are outputted as pri (red), sec (green) and ter (blue).
 
•	Excel file/sheet (lines 17-18): do not need to be created prior to programme run.
Define data to export:
 
•	Include desired regions/colours (lines 78-81).
OCR
OCR programme is fairly complex and will need to be specifically altered to fit each experiment.
General parameters 
Insert parameters (lines 11-20) and specify location of tesseract programme (line 22):
 
•	Directory (line 12): input directory name where photos are located. Do not include any files which are not to be analysed.
•	Paths should be inputted as r’path_name’. Removing the r will cause the programme to break.
•	Use show_first_pic as “Y” or “Yes” to aid setting parameters for image simplification (see below).
•	Excel file/sheet (lines 19-20): do not need to be created prior to programme run.
Image simplification
The OCR first requires simplifying the image to improve text recognition. The editable simplifications are cropping, deskewing, thresholding, eroding and dilating:
•	Cropping (line 13) and deskewing (line 14) should be self-explanatory.
 → → 
•	Thresholding (line 15) changes all pixels below a certain thresholding white and all those above black. The greater the threshold value, the lighter the pixels that are accepted as black. The value used will depend on the display/lighting.
  
•	Eroding (line 16) increases the boundaries of black objects, allowing the separate segments to merge. This is important as OCR detects characters as a complete objects. The greater the number of iterations, the wider the boundaries will become. The parameters used will depend on the display.
 
•	Dilating (line 17) decreases the boundaries of the black objects, but will not separate the segments that were previously merged. The greater the number of iterations, the narrower the boundaries will become. The parameters used will depend on the display.
  
Currently, the OCR programme searches exclusively for digits 0-10. This does not include symbols such as a minus sign or a decimal points. These are put in later (output manipulation). However, other characters can be added into the “whitelist” (see below). The psm number (currently 7) changes the type of text the programme is looking for. 7 should be suitable for most applications here but could be changed if required (guides available online).
 
From this, numbers will be outputted. However, the recognition software is not perfect and does make frequent mistakes. For example, it often mistakes 0 for 6 or 8. Therefore, some cheats are included to fix some of the most easily fixed mistakes.
Output manipulation
Several corrections are applied to the outputted number. For example, if the first digit (tens) is read as 8, it is automatically changed to a 0, because all readings were <6. These manipulations are largely explained between lines 88-216. Fewer/further/new manipulations may be required for different displays/results.
Checking
Some mistakes cannot be easily accounted for. This is especially true for photographs taken between meter readings, where both digits are simultaneously visible. Therefore, these outputs should be checked by hand if publicised.
Some mistakes can be very easily spotted by graphing. E.g.:
 
Fixing the five biggest offenders:
 
For the starred peak above:
