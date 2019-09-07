Python - Pipfile with python_version and runtime.txt
----------------------------------------------------

We are ignoring the runtime.txt if there is a Pipfile or Pipfile.lock available.
And since `python_version = "3.6"` in the Pipfile, the `python-3.7` in
runtime.txt should be ignored. Is it?
