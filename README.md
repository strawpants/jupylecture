# Creating lectures using jupyter notebook slides with RISE and reveal.js

You can run the first 'lecture' in an interactive jupyter notebook here [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/strawpants/jupylecture/master?filepath=jupylecture/templates/ITCTemplateBlack.ipynb)

The [RISE extension](https://rise.readthedocs.io/en/stable/support.html) allows you to run reveal.js presentations with embedded code cells from jupyter.
The **jupylecture** module adds functionality to the default RISE functionality, such as for example more freedom in placing content on the slides by using flexboxes.


## Installation
Clone the [jupylecture repository](https://github.com/strawpants/jupylecture) and install using pip (possibly in your dedicated virtual environment)
```
git clone https://github.com/strawpants/jupylecture 
pip install jupylecture
```

## Initializing a new lecture setup
Navigate to a suitable destination direction and initialize the lecture files:
```
mkdir testlecture
cd testlecture
jupylectureinit.py NewLecture.ipynb
```
After initialization you can start a jupyter instance and navigate to the notebook

## Tips and Tricks
* Enable fullscreen when developing the lecture in a browser, this ensures that the aspect ratio of your lecture will be correct. 
* A [bash script to export the notebooks](jupylecture2pdf.sh) is provided to convert the presentation to a pdf format
* For developers: When an editable installation has been performed (`pip install -e jupylecture`) it's possible to add the `--develop` flag to [jupyterinit.py](jupyterinit.py), so the css files and image files are symlinked instead of copied. This allows parallel development of lectures and this module (e.g. no need to update rise.css)


## Todo
* Publish on pypi when this package is a bit more mature
* Enable a static export to html

