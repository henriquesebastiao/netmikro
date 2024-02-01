![logo do projeto](assets/netmikro.svg){ width="100"}
# Netmikro

Netmikro is a simple library that provides an easy way to manage Mikrotik routers, simplifying configuration and monitoring tasks.

Everything works through an instance of the RouterOS class that creates an SSH connection with the device, think of the instantiated object as your own router, this object has [methods](api/RouterOS.md) to interact with your router, or you can Run custom commands directly in your router's terminal with the `cmd()` method.

Netmikro is on the shoulders of the [Netmiko](https://github.com/ktbyers/netmiko) project, responsible for creating a connection via SSH with the Mikrotik router.

!!! note

    I'm just a computer networking enthusiast and have experience with handling MIkrotik routers.
    All Netmikro features are being tested during development with a Mikrotik RB912UAG-5HPn router.
    The idea is to test it on other models as soon as possible.

---

**Documentation**: [https://netmikro.henriquesebastiao.com](https://netmikro.henriquesebastiao.com)

**Source Code**: [https://github.com/henriquesebastiao/netmikro](https://github.com/henriquesebastiao/netmikro)

---

## How to install

Netmikro is available on PyPi, so just use your preferred package manager:

``` {.bash .copy }
pip install netmikro
```

## Basic usage

You just need to create an instance of RouterOS to use Netmikro features:

```Python
from netmikro import RouterOS


router = RouterOS(
    '192.168.3.3',
    'user',
    'password',
    22,
)

router.cmd('/system identity print')
```

## License

This project is licensed under the terms of the MIT license.
