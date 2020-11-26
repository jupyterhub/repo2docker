Python - Pipfile including `jupyter` as dependency
--------------------------------------------------
When `jupyter` is listed as dependency, we still should be able to run the 
container. `repo2docker` delegates the jupyter notebook execution to the
`pipenv` virtualenv in this case

