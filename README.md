# Monitorimittari

## Install python 3

https://www.python.org/downloads/

## Install and create virtualenv

`pip install virtualenv`
`virtualenv venv`

## Activate virtualenv

* On windows 
  
 `venv/Scripts/activate`

* On linux 
  
 `source venv/Scripts/activate`

## Deactivate virtualenv

`deactivate`

## Install requirements

`pip install -r requirements.txt`

## Edit ui with pyqt5 designer

`venv/Lib/site-packages/pyqt5_tools/designer.exe ui.ui`

## Generate ui file

`venv/Scripts/pyuic5.exe -x ui.ui -o ui.py`

## build and install exe file

`python install.py`

## PyQt5 tutorial

https://youtu.be/ksW59gYEl6Q

## Threading how-to

https://www.mfitzp.com/article/multithreading-pyqt-applications-with-qthreadpool/
