# Local Server Setup

These instructions are for setting up a local RootPainter server. If you do not have a suitable NVIDIA GPU with at least 8GB of GPU memory, the current recommendation is to use the [Google Colab tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing).

For other remote server setups, see the [sshfs server setup tutorial](../setup/remote_server_sshfs.md). You can also use Dropbox instead of sshfs.

For the next steps I assume you have a suitable GPU and CUDA installed.

1. To install the RootPainter trainer:

    ```
    pip install root-painter
    ```

2. To run the trainer. This will first create the sync directory.

    ```
    root-painter trainer
    ```

    !!! note
        if you are installing the RootPainter trainer (server) from scratch on windows 11 I suggest [these linked instructions](../setup/windows_trainer.md).

    You will be prompted to input a location for the sync directory. This is the folder where files are shared between the client and server. For example, you can use `~/root_painter_sync`.
    RootPainter will then create some folders inside your sync directory. The server should print the automatically selected batch size, which should be greater than 0. It will then start watching for instructions from the client.

    You should now be able to see the folders created by RootPainter (datasets, instructions and projects) inside the sync directory on your local machine.

    For an example of how to use RootPainter to train a model, see the [lung tutorial](../tutorials/cxr_lung.md). It is now recommended to follow the [Colab tutorial](https://colab.research.google.com/drive/104narYAvTBt-X4QEDrBSOZm_DRaAKHtA?usp=sharing) instructions but using your local setup instead of the colab server, as these are easier to follow than the lung tutorial.
