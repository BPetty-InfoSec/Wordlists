# Wordlists

This project was (re)created to help manage wordlists for use in pentesting engagements.

Originally, this project was written in Python, re-written in Go, and went back to Python.
This was all on the same (main) branch of the repo. I didn't really know Git at the time
(OK, so I _still_ don't really know Git, but it's better than it was) and the timeline
had gotten so confusing that it just wasn't worth trying to figure it out.
Given that, I deleted the repo, and re-created it here.

Essentially, what this application will do is travel through a list of sub-directories that
are full of wordlists for use in various applications. These wordlists can be given categories
that they belong to as they are picked up and processed for the first time. These categories can
then be modified later, if desired. In an output directory, there will be a sub-directory
for each category, containing symlinks to the corresponding original wordlist in the library
directory.
