# Folder content summary

A tiny script that summarizes the files inside a folder (including subfolder)
and outputs the file's path, SHA256 hashsum, last modified date and size (in bytes) to a csv.

The motivation for this script is comparing folders on different system
without having to have access to both folders at the same time. This can be used for example
to try and scrap together files from multiple different systems to restore a wiped cloud.

It summarizes the current working directory into a `summary.csv` file (also in that directory, watch for conflicts). Quick and dirty but it works great. Feel free to adjust it to your needs.

Ps. it did what it was supposed to but there were some encoding issues as well as platform dependent path delimiters, so maybe fix that before using or you'll have to do it in post :)

## Usage

```shell
cd to/your/folder
python to/this/repo/summarize_folder.py
```

## License

"No Rights Reserved"

CC0 (Public Domain)
