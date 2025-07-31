# Use a community-maintained image in a JupyterHub

The simplest way to deploy environment images to a JupyterHub or BinderHub is to _find and re-use a pre-existing image maintained by a community_. In this case, you won't have to maintain anything - you'll simply use a community's image and contribute upstream if you wish.

Here are some steps to follow.

## First, find a community-maintained image for your workflow

Many communities define their own user envionment images for re-use. Here are a few to look into.

1. [jupyter docker-stacks](https://jupyter-docker-stacks.readthedocs.io/) has a number of user images for general data science workflows.
2. [pangeo docker-stacks](https://github.com/pangeo-data/pangeo-docker-images) has images for geospatial workflows in the cloud
3. [rocker](https://rocker-project.org/) has images meant for reproducibility with the R computing language.

For example, the [Jupyter Docker Stacks images](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#core-stacks) define images for several core datascience workflows. Each one points to a **hosted version of the image** on an image repository (such as [quay.io](https://quay.io)).

## Pick a tag for the image

Tags are a way to checkpoint an image so that you know exactly what is inside. They are similar to released versions of software. Tags will be listed in the image provider used by the community. For example:

[Here's the list of tags for the `docker-stacks-foundation` image](https://quay.io/repository/jupyter/docker-stacks-foundation?tab=tags).

:::{admonition} Don't use the `latest` tag
:class: warning
`latest` is a special tag for "the latest tag to be released". This is generally a bad idea when using environment images for your interactive data science sessions. Here are a few reasons why:

- The environment may regularly change without warning as new versions of the image are released.
- The `JUPYTER_IMAGE` environment variable will not be useful because it's a generic `latest` variable.
- If you use tools that _themselves_ use Docker, you might have different images on your interactive environment vs. the images the tools use, because they haven't all updated at once.

Instead, we recommend periodically manually updating the tag you use over time.
:::

## Configure JupyterHub to use the tag

Once you have an image and a tag, you can configure your JupyterHub to use it.

Here's sample configuration if you're using the [Zero to JupyterHub for Kubernetes distribution](https://z2jh.jupyter.org).

```yaml
singleuser:
  image:
    name: pangeo/pangeo-notebook
    tag: 2023.04.15
```

Here's sample configuration if you're using the [Dockerspawner for JupyterHub spawner](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/).

```python
c.DockerSpawner.image = 'pangeo/pangeo-notebook:2023.04.15'
```

When you re-deploy your JupyterHub application, it should now spawn user environments from the image you've configured.
