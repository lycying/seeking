========
Download
========
There are typically two types of Seeking releases: a "stable" release
and a "development" release.  If you are new to Seeking, you almost
certainly want to use the "stable" Seeking release.

Download
=========

 * `seeking-0.1_win32.7z  <http://code.google.com/p/seeking/downloads/list>`_  for windows only
 * `seeking-0.1_source.tar.gz  <http://code.google.com/p/seeking/downloads/list>`_ 
 * `seeking-0.1_source.zip  <http://code.google.com/p/seeking/downloads/list>`_ 

(1) ``.7z`` Use the program 7-zip that with High compression ratio, can uncompress with 7-zip or winrar 
(2) ``.tar.gz`` Uses the tar program to gather files together, and gzip to compress and uncompress.
(3) ``.zip`` Recommended compression format for Windows, can also be used on other platforms. Supported by many programs and some operating systems natively.

If you prefer the source edition, you can download the source for the latest current version. If you prefer the leading-edge code, you can access the code as it is being developed via SVN. The google website has details on accessing SVN.  everything other than new features are usually stable.
The latest revision can be obtained like this::

  $ svn checkout http://seeking.googlecode.com/svn/trunk/ seeking

Install
=======
 * You may download Seeking from http://code.google.com/p/seeking/downloads/list , from which the most recent stable versions are always available in the Download area.
 * Uncompress the downloaded file into a directory.

windows
-------
Just double click the ``Seeking.exe`` to start up Seeking

if you are using the source version . flow the source installing part 

from source
-----------
Make sure you have a python and pyqt environment installed.

 * ``Python2.6`` http://www.python.org/download/
 * ``PyQt4 bind python2.6`` http://www.riverbankcomputing.co.uk/software/pyqt/download

command::

  $ wget -c http://code.google.com/p/seeking/downloads/list/seeking-*_source.tar.gz
  $ tar xvf seeking-*_source.tar.gz
  $ cd seeking-*_source/
  $ ./start-seeking



