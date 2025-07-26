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
EXPORT VARIABLE ["
Welcome to my love program!
"]
CONFIGURE["readme", VARIABLE]
-> Version, Optional
CONFIGURE["version", "1.0"]
```
