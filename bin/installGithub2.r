#!/usr/bin/env r

suppressMessages(library(docopt))
suppressMessages(library(devtools))

doc <- "Usage: installGithub.r [-h] [-d DEPS] [-r GIT_REF] [-t GITHUB_TOKEN] REPOS...

-h --help                   show this help text
-d --deps DEPS              Install suggested dependencies as well? [default: NA]
-r --ref GIT_REF            Git ref [default: master]
-t --token GITHUB_TOKEN     Github token

where REPOS...        is one or more GitHub repositories.
where GIT_REF...      is a Git ref i.e. master, v1.0.
where GITHUB_TOKEN... is a GitHub auth token.

Examples:
  installGithub.r RcppCore/RcppEigen -r v1.0 -t eeb9c8a5f416f7cfe982734440e39fa72abbcb33
"

opt <- docopt(doc)
if (opt$deps == "TRUE" || opt$deps == "FALSE") {
    opt$deps <- as.logical(opt$deps)
} else if (opt$deps == "NA") {
    opt$deps <- NA
}

invisible(sapply(opt$REPOS, function(r) install_github(repo=r, dependencies=opt$deps, ref=opt$ref, auth_token=opt$token)))
