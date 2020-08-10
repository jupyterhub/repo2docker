==========================
Add a new content provider
==========================

Adding a new content provider allows repo2docker to grab repositories from new
locations on the internet. To do so, you should take the following steps:

#. Sub-class the `ContentProvider class <https://github.com/jupyterhub/repo2docker/blob/master/repo2docker/contentproviders/base.py#L17>`_.
   This will give you a skeleton class you can modify to support your new
   content provider.
#. Implement a **detect()** method for the class. This takes an input
   string (e.g., a URL or path) and determines if it points to this particular
   content provider. It should return a dictionary (called
   ``spec`` that will be passed to the ``fetch()`` method. `For example, see the ZenodoProvider detect method <https://github.com/jupyterhub/repo2docker/pull/693/files#diff-a96fcf624176b06e21c3ef7f6f6a425bR31>`_.
#. Implement a **fetch()** method for the class. This takes the dictionary ``spec`` as input, and
   ensures the repository exists on disk (e.g., by downloading it) and
   returns a path to it.
   `For example, see the ZenodoProvider fetch method <https://github.com/jupyterhub/repo2docker/pull/693/files#diff-a96fcf624176b06e21c3ef7f6f6a425bR57>`_.
