## Obtaining `python3`

Most modern operating systems, to the exception of Windows, come with `python3` pre-installed.

If you are using Windows, you can try [this method](https://lmgtfy.com/?q=install+python3+on+windows).

Otherwise if you are using on old version of Linux or macOS, you can simply install your own version of python in your home directory without administrator privileges. To do this we suggest using this excellent project along with it's installer:

* https://github.com/yyuu/pyenv
* https://github.com/yyuu/pyenv-installer

In essence, you just need to type this command:

    $ curl https://pyenv.run | bash

And then add these lines to your ``.bash_profile`` file:

    $ vim ~/.bash_profile

        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"

Finally, relaunch your shell for changes to take effect and type these commands to get the right version of python:

    $ pyenv install 3.8.6
    $ pyenv global 3.8.6
    $ pyenv rehash

## Obtaining `pip3`

If you are using a recent Ubuntu or Debian operating system and are an administrator of the computer, the following commands should install `pip3` onto your computer:

    $ sudo apt-get update
    $ sudo apt-get install python3-pip

Otherwise, if that doesn't succeed, you can attempt this more generic method that works with a wider range of configurations and doens't require the sudo command. Use the `get-pip` script like so:

    $ curl -O https://bootstrap.pypa.io/get-pip.py
    $ python3 get-pip.py --user

If you still did not succeed, check that you have the following required package installed before running the `get-pip` script again:

    $ sudo apt-get update
    $ sudo apt-get install python3-distutils
