#!/usr/bin/env Rscript
library('digest')


# Fail if version isn't 4.2, the default version for the RBuildPack
print(version)
if (!(version$major == "4" && as.double(version$minor) >= 2 && as.double(version$minor) < 3)) {
  quit("yes", 1)
}
