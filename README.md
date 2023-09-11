[![Status](https://img.shields.io/badge/Status-development-red)](https://github.com/henriquesebastiao/netmikro)
[![LICENSE](https://img.shields.io/github/license/henriquesebastiao/netmikro)](https://github.com/henriquesebastiao/netmikro/blob/main/LICENSE)

<img src="docs/assets/netmikro.svg" width="150">

# Netmikro

Library to simplify MikroTik device configurations.

## Use

```python
from netmikro import RouterOS

router = RouterOS(
    host='192.168.88.1',
    username='admin',
    password='admin',
    port=22,
    delay=0.5,
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
