Docker - Running scripts
------------------------

It's possible to run scripts using Docker in your build. In this case, we run
a simple shell script after installing dependencies.

While it's possible to run code with Dockerfiles, we recommend
that try accomplishing the same thing with ``apt.txt`` and
``postBuild`` files. Only use Dockerfiles when necessary.
