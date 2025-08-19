#!/usr/bin/env Rscript
library('digest')


# Fail if version isn't 4.4, the default version for the RBuildPack
print(version)
if (!(version$major == "4" && as.double(version$minor) >= 4 && as.double(version$minor) < 5)) {
  quit("yes", 1)
}
