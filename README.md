## RootPainter

RootPainter is a GUI-based software tool for the rapid training of deep neural networks for use in image analysis. 
RootPainter uses a client-server architecture, allowing users with a typical laptop to utilise a GPU on a more computationally powerful server.  

A detailed description is available in the paper published in the New Phytologist  [RootPainter: Deep Learning Segmentation of Biological Images with Corrective Annotation](https://doi.org/10.1111/nph.18387)

![RootPainter Interface](https://user-images.githubusercontent.com/376295/224013411-cb44c7c2-5c72-4819-98a3-6c0ab8b9ea4d.png)

To see a list of work using (or citing) the RootPainter paper, please see the [google scholar page](https://scholar.google.com/scholar?cites=12740268016453642124)

A BioRxiv Pre-print (earlier version of the paper) is available at:
[https://www.biorxiv.org/content/10.1101/2020.04.16.044461v2](https://www.biorxiv.org/content/10.1101/2020.04.16.044461v2)


### Getting started quickly

I suggest the [colab tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing).
 
A  shorter [mini guide](docs/mini_guide.md) is available including more concise instruction, that could be used as reference. I suggest the paper, videos and then colab tutorial to get an idea of how the software interface could be used and then this mini guide for reference to help remember each of the key steps to get from raw data to final measurements. 
 
### Videos

A 14 minute video showing how to install RootPainter on windows 11 with google drive and google colab is available on [youtube](https://www.youtube.com/watch?v=HuSujZQOkQw). A similar video for macOS is also [now available on youtube](https://youtu.be/rBCkem0ub_I). I suggest watching these videos to help with the installation part of the [colab tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing).

A video demonstrating how to train and use a model is available to [download](https://nph.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1111%2Fnph.18387&file=nph18387-sup-0002-VideoS1.mp4)

There is a [youtube video](https://www.youtube.com/watch?v=73u73tBvRO4) of a workshop explaining the background behind the software and covering using the colab notebook to train and use a root segmentation model.

---

### Installation

#### Server

Install from PyPi:

```bash
pip install root-painter-trainer
```

#### Client

Go to [releases](https://github.com/Abe404/root_painter/releases/latest) and download install the client for your platform. 

or install directly with python

```bash
# install to start from form with uv
uv tool install -p 3.10 git+https://github.com/jakob1379/root_painter@jga-end-goal#subdirectory=painter

# similarly with pipx - you need to figure out how to install the correct python yourself - uv does this for you.
pipx git+https://github.com/jakob1379/root_painter@jga-end-goal#subdirectory=painter

# now you can always do
root-painter
```

If you are not confident installing and running python applications on the command line then to get started quickly I suggest the [colab tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing).

### Documentation

Comprehensive documentation, including setup guides, tutorials, and developer information, is available in the [`docs/`](docs/) directory.

- **Getting Started:** For a quick start, we recommend the [Colab Tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing). A concise [Mini Guide](docs/mini_guide.md) is also available for quick reference.
- **Server Setup:** Instructions for setting up the server component are available for [local installations](docs/server_setup_local.md), [sshfs setups](docs/server_setup_sshfs.md), and more.
- **Tutorials:** See the [lung segmentation tutorial](docs/cxr_lung_tutorial.md) for a practical example.
- **FAQ:** Check the [Frequently Asked Questions](docs/FAQ.md) for answers to common issues.

### For Developers

Developer-focused documentation, including build instructions and contribution guidelines, can be found in `docs/dev/`.

- [Painter (Client) Readme](docs/dev/painter_readme.md)
- [Trainer (Server) Readme](docs/dev/trainer_readme.md)


 ### Questions and Problems
 
The [FAQ](docs/faq.md) may  be worth checking before reaching out with any questions you have. If you do have a question you can either email me or post in the [discussions](https://github.com/Abe404/root_painter/discussions). If you have an issue/ have identified a problem with the software then you can [post an issue](https://github.com/Abe404/root_painter/issues).
