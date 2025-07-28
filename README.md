# four
Four is an Application Maker! Made with the help of Jehovah!
For make your first app, It need to include:

Project Name
Avaliabe platform
Run command

Let's see with love an example!

```four
-> example.four

-> Project Name
PROJECT "Example"

-> Configuration
CONFIGURE["platform", "all"]
CONFIGURE["run", "python3"]

-> Code
DEFINE MAIN
print('Welcome to my application of four! Made with love with the help of Jehovah!')
```

To run it! You need to compile it first! with:

```bash
four build example.four
```

And then!

```bash
four run Example.app
```

In "PROJECT", You can set any name, In "CONFIGURE" There's four configurations:

```four
-> Avaliabe Platform
CONFIGURE["platform", "linux"]
-> Run with
CONFIGURE["run", "lua"]
-> README, Optional
CONFIGURE["readme", "Welcome to my application!"]
-> Version, Optional
CONFIGURE["version", "1.0"]
```

# How to install four with love

To install four, execute:

```bash
curl -s https://raw.githubusercontent.com/zer0users/four/refs/heads/main/install.sh | bash
```

It will install four with love.

# Four Example (1.0)

```four
-> example.four

PROJECT "Example"

CONFIGURE["platform", "linux"]
CONFIGURE["run", "python3"]

DEFINE MAIN
print('Welcome to my application!')
import tkinter

root = tkinter.Tk()
root.title('Love Example')
root.mainloop()
```

How to compile:

```bash
four build example.four
```


# Four Example (1.1)

```four
-> example.four

PROJECT "Example"

CONFIGURE["platform", "linux"]
CONFIGURE["run", "python3"]

-> Please replace "user" to your user name! :D

FOLDER "love"
FILE "/home/user/file.txt" "love/file.txt"

DEFINE MAIN
file = open('love/file.txt').read()
print(file)
```

How to compile:

1. Please modify "user" to your user name.
2. And add an "file.txt" in your home.

```bash
four build example.four
```

# Avaiable Operating Systems: Four

Four is avaiable for Linux, The windows version is in deveploment.

Linux install:

```bash
curl -s https://raw.githubusercontent.com/zer0users/four/refs/heads/main/install.sh | bash
```

Windows:

```powershell
iwr -useb https://raw.githubusercontent.com/zer0users/four/refs/heads/main/windows-install.ps1 | iex
```
Please be aware in this Windows version, the installer has NOT been tested, if you are sure to install four for windows, read his content first please
But remember, God is with you, Trust him
