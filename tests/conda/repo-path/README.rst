Python - Custom Repository Location
-----------------------------------

We want to support custom paths where repositories can be
copied to, instead of ${HOME}. The `extra-args.yaml` file in
each dir can contain a list of arguments that are passed
to repo2docker during the test. We copy this repo to
/srv/repo instead of ${HOME}