Docker - Running scripts
------------------------

It's possible to run scripts using Docker in your build. In this case, we run
a simple shell script after installing dependencies. However, we recommend
that you see if it's possible to accomplish what you want using ``apt`` and
``postInstall`` files, and use Dockerfiles only when necessary.
