0.5.0 - Efficiency First
========================

* Refactor to improve response times dramatically
    * Previously, results relied on a local git clone of the repo but this was very slow in almost all cases
    * Now, all data is pulled from Github API
    * "Advanced data" that requires cloning the git repo may return in the future
* Previously, site supported links to both Github and Bitbucket but now only supports Github URLs
    * Bitbucket support (or other popular Git sites) may return in the future


0.6.0 - Features Return
=======================

* Add back support for longer running metrics
* Fixed bug finding the latest commit if that commit was over 6 months ago
* Added support for pull request data
