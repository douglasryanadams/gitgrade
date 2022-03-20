5.0.0 - Efficiency First
========================

* Refactor to improve response times dramatically
    * Previously, results relied on a local git clone of the repo but this was very slow in almost all cases
    * Now, all data is pulled from Github API
    * "Advanced data" that requires cloning the git repo may return in the future
* Previously, site supported links to both Github and Bitbucket but now only supports Github URLs
    * Bitbucket support (or other popular Git sites) may return in the future
