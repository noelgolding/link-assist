# Link Assist
## Copy the code to your desktop
1. Open a text editor
1. Copy and paste the code from [ftp_links.py](ftp_links.py)
1. Save the file as `filezilla_links.command` to your Desktop 

## Enable clicking the Desktop icon to execute it
Open a terminal window
```shell
cd ~/Desktop
chmod +x filezilla_links.command
```

## If you have not already done so, prep your filezilla directory
1. Create a folder on your Desktop named `filezilla` (notice case, spaces, spelling matters)
1. Create subfolders in `filezilla` for your pdfs. eg. outlet, specialty, etc.
1. Copy all the pdfs to the appropriate subfolders

Your directory structure should look like:
```text
$HOME/Desktop/filezilla/
├── speciality
│    ├── This is one stylesheets.pdf
│    └── this IS two.pdf
└── outlet
     └── AnoTher PDF employee's guide.pdf
```

After your run the code your directory structure will look like:
```text
$HOME/Desktop/filezilla/
├── speciality
│    ├── this_is_one_stylesheet.pdf
│    └── this_is_two.pdf
└── outlet
     └── another_pdf_employee_guide.pdf
```

## Run the code!
Double-click the icon on your Desktop

## What happened? I don't see anything :(
If a browser window does not open, try pasting this url into a browser tab   
You can preview this output for typos etc, however the links will not work until you ftp the files.
```text
~/Desktop/filezilla/links.html
```

## Ftp your files and folders
Use filezilla to upload your directories and pdfs

## Test out the links
```text
~/Desktop/filezilla/links.html
```

## Update the links in the LMS
You should be able to copy and paste from the `links.html` file into the LMS
