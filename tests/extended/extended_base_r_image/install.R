#!/usr/bin/env Rscript

# Function to install any of the given packages that aren't already installed.
install_packages <- function(packages) {
  to_install <- packages[!(packages %in% rownames(installed.packages()))]

  if (length(to_install) > 0) {
    install.packages(to_install, dependencies = TRUE)
  } else {
    cat("All packages are already installed.\n")
  }
}

# List of packages to ensure are installed
required_packages <- c("remotes", "devtools")

# Check and install required packages
new_packages <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]
if (length(new_packages) > 0) {
  install.packages(new_packages)
}

packages <- c(
  "AER",
  "BH",
  "BiocManager",
  "DBI",
  "FNN",
  "R.methodsS3",
  "R.oo",
  "R.utils",
  "RCSF",
  "RCurl",
  "RNetCDF",
  "RcppProgress",
  "assertthat",
  "bibtex",
  "bindrcpp",
  "broom",
  "crosstalk",
  "data.table",
  "devtools",
  "dichromat",
  "e1071",
  "forcats",
  "future",
  "gdtools",
  "geoR",
  "geometry",
  "geosphere",
  "ggplot2",
  "globals",
  "gstat",
  "haven",
  "hdf5r",
  "hms",
  "htmlwidgets",
  "intervals",
  "jsonlite",
  "units",
  "leafem",
  "leafpop",
  "leafsync",
  "learnr",
  "lfe",
  "linprog",
  "listenv",
  "lpSolve",
  "lubridate",
  "lwgeom",
  "magic",
  "manipulateWidget",
  "mapdata",
  "mapproj",
  "mapview",
  "matrixStats",
  "modelr",
  "ncdf4",
  "ncmeta",
  "nlme",

  # polsci 3, fall 2026, https://github.com/berkeley-dsep-infra/datahub/issues/8375
  "ottr",
  "packrat",
  "pander",
  "pbdZMQ",
  "png",
  "proj4",
  "proto",
  "pryr",
  "rapportools",
  "raster",

  # polsci 3, fall 2026, https://github.com/berkeley-dsep-infra/datahub/issues/8135
  "rdrobust",
  "readr",
  "readxl",
  "rematch",
  "remotes",
  "repr",
  "reprex",
  "reshape",
  "reticulate",
  "rjson",
  "rlas",
  "rlist",
  "rpart",
  "rsconnect",
  "satellite",
  "selectr",
  "spacetime",
  "spatialreg",
  "spatstat",
  "spatstat.data",
  "spdep",
  "splancs",
  "stargazer",
  "summarytools",
  "svglite",
  "testit",
  "tidync",
  "tidyr",
  "tmap",
  "tmaptools",
  "tufte",
  "utf8",
  "uuid",
  "vroom",
  "whoami",
  "widgetframe",
  "withr",
  "xfun",
  "xts",

  # dplyr packages
  "dplyr",
  "arrow",
  "dbplyr",
  "dtplyr",
  "nycflights13",
  "Lahman",
  "RMariaDB",
  "RPostgres",
  "RSQLite",
  "fst",
  # /dplyr packages

  # publishing packages
  "blogdown",
  "rticles",
  "xaringan",
  # /publishing packages

  # https://github.com/berkeley-dsep-infra/datahub/issues/4907
  # "Fall '23 and beyond"
  "mosaicData",

  # polsci 3, fall 2026
  # https://github.com/berkeley-dsep-infra/datahub/issues/8376
  "estimatr",

  # From https://github.com/berkeley-dsep-infra/datahub/issues/3757
  # econ 140, fall 2022 and into the future
  "ipumsr",

  # https://github.com/berkeley-dsep-infra/datahub/issues/6545
  # ENVECON 118, Spring 2025
  "gridExtra",
  "magrittr",
  "margins",
  "openxlsx",
  "quantmod",
  "QuantPsyc",
  "qwraps2",
  "sandwich",
  "stats",

  # DH-446, Econ 140, Spring 2025
  "wooldridge",

  # Used when developing the gradebook app
  # https://github.com/andrewpbray/gradebook-app
  # For Spring '25 into the future
  "Hmisc",
  "purrr",
  "shinyFiles",
  "shinyTime",
  "shinyWidgets",
  "shinydashboard",
  # /gradebook packages

  # DH-484, PS 137, Spring 2025
  "coefplot",

  # When adding or removing packages, note that the last package in this list
  # should not have a trailing comma, but every other package should.

  # When adding, try first installing the package within a datahub session to
  # verify it's actually available on the snapshotted package repository.

  # DH-553 , MBA 247, Fall 2025
  "arules",
  "arulesViz",
  "caret",
  "factoextra",
  "imager",
  "pROC",
  "randomForest",
  "rpart.plot",
  "SnowballC",
  "tm",
  "wordcloud",
  "xgboost",
  "SentimentAnalysis",

  # DH-722
  "googlesheets4"
)

install_packages(packages)

## Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

# Posit Package Manager currently has no binary BioConductor packages.
BiocManager::install("rhdf5")
BiocManager::install("Rhdf5lib")
