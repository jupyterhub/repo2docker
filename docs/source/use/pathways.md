# Four ways to use `repo2docker` images in a JupyterHub

Many users of `repo2docker` primarily wish to define the environment for a Binder or a JupyterHub. Here are four ways to accomplish this, from least-to-most work.

```{figure} ../_static/images/whentouse.svg
A decision tree for the recommended way to get your reproducible user environment using `repo2docker` or a community image built with `repo2docker`.
```

## 1. Use a community maintained image

The simplest thing to do is check whether another community already maintains and offers an image that you can simply re-use. This reduces the burden on you to keep the image up-to-date, and gives you an opportunity to collaborate and make contributions rather than building something yourself from scratch.

See [](./community-image.md) for a brief how-to on using a community maintained image.

::::{grid} 2
:::{grid-item-card} Benefits

- A community of experts maintains the image with you!
- Don’t struggle alone with your problems, drag others along!
- Good choices (base image, how python is installed, etc) made on your behalf
- Updates happen without you needing to do much
  :::
  :::{grid-item-card} Drawbacks
- Might have lots of stuff you don’t need
- Large image sizes, slower pulling
- Might get you 98% of the way there, but that ain’t 100%
- Architectural choices made might not fit your use case
- Updates are not on your schedule
  :::
  ::::

## 2. Inherit from a community maintained image and add a few extras

Sometimes a community-maintained environment image has **almost** what you need, but there are a few extra packages you'd like to install yourself. In this case, it's easiest to **inherit and extend the community image**.

This is not the same thing as forking the repository for the community image, modifying it, and re-building it from scratch. It's similar to depending on an upstream piece of software and then building upon it in your own tool.

::::{grid} 2
:::{grid-item-card} Benefits of inheriting and adding to community images

- Only need to maintain the changes you make
- Update the FROM tag to keep up with upstream changes
- You must manage a GH repo
- Works well with mybinder.org
  :::
  :::{grid-item-card} Drawbacks of inheriting and adding to community images
- Need to understand how upstream image is built so you can customize
- Documentation for this method currently sucks (but can be fixed!)
- Removing existing packages might break things
- You must manage a GH repo
  :::
  ::::

See [](./extend-community-image.md) for a how-to guide.

## 3. Use repo2docker to build your environment image

If your needs differ far enough from the community-maintained images that you find, you can use `repo2docker` to build your environment image using [supported configuration files](#config-files).
To learn how to do this, follow the [getting started with repo2docker guide](../start.md) and look at the [list of supported configuration files](#config-files).
Check out the other sections under "Image building basics" for more useful how-tos.

::::{grid} 2
:::{grid-item-card} Benefits

- Works well with mybinder.org
- No need to learn Dockerfile syntax
- Use language specific, well understood file formats
- Only get whatever packages you want
- Good defaults chosen by the community
  :::
  :::{grid-item-card} Drawbacks community-maintained images
- Build time is slower
- Images may be bigger
- Might not support 100% of what you want, and at some point you might have to take the ramp-off to a Dockerfile
  :::
  ::::

## 4. Use a full fledged custom Dockerfile

If you need full control over the entire computational environment, you can always create your own `Dockerfile` from scratch, and repo2docker will build an image out of it.

This is for advanced users only that know what they're doing - full guidance on how to use `Dockerfiles` is out of scope for this tutorial.

[Here's an example repository that uses a `Dockerfile` to build with repo2docker].

::::{grid} 2
:::{grid-item-card} Benefits of community-maintained images

- Get exactly what you want
- Can be optimized for small image size & fast build times
- Lots of existing documentation in the SRE world on how to use these

:::
:::{grid-item-card} Drawbacks of community-maintained images

- Requires a lot of knowledge for ongoing maintenance
- Might have to solve problems yourself that were solved in upstream images / repo2docker
- Need to adapt existing documentation from the SRE use case to interactive computing use case
  :::
  ::::
