# Timeclocks
A simple Python utility for timing a handful of processes.

## Usage
![Timeclocks](https://i.ibb.co/W3LYwRQ/Timeclocks.gif)

- Toggling Syncronous vs Asynchronous will allow/disallow the ability for all stopwatches to run in parallel.
- The "Change Category" button will allow renaming of each stopwatch category.
- Ctrl + S will allow for saving timed results into a .txt file.

## Building

If you'd like to build the standalone executable, I've included the PyInstaller .spec file to accomplish that for you. To build a new .exe, open a command prompt window in the project directory and run the following:

```python
pyinstaller build.spec
```
When PyInstaller finishes running, the new .exe file will be located in /dist. You may need to run 'pip install pyinstaller' if you don't already have it.

## License
[MIT](https://choosealicense.com/licenses/mit/)
