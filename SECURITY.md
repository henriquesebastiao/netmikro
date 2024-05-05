# Security Policy for Netmikro

## Overview

Netmikro is a Python API designed for managing Mikrotik routers. This policy outlines the security measures and
procedures to ensure the safe usage and development of the project. The goal is to protect the Netmikro community and
users from potential threats.

## RouterOS version support

| Version | Supported  |
|---------|------------|
| 7.14.3  | ✅          |
| Others  | Not tested |

## Reporting Vulnerabilities

If you discover a vulnerability in Netmikro, please report it immediately by sending an email to [security@henriquesebastiao.com](mailto:security@henriquesebastiao.com). Include the following details:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested mitigation or fix

I (the maintainer, [@henriquesebastiao](https://twitter.com/hick_hs)) will fully review it and get back to you.

## Security Best Practices

When using Netmikro, follow these best practices to safeguard your environment:

1. **Network Security**: Ensure that routers managed by Netmikro are on a secure network and protected by a firewall.
2. **Updates and Patching**: Keep Netmikro and dependent libraries up to date to receive the latest security fixes.
3. **Logging and Monitoring**: Enable logging to detect suspicious activities and monitor for any unauthorized access.

## Development Guidelines

1. **Code Review**: All code changes must go through a thorough review process.
2. **Dependency Management**: Regularly audit dependencies for known vulnerabilities.
3. **Static Code Analysis**: Use static analysis tools to detect security issues during development.
4. **Testing**: Develop comprehensive tests, including unit and integration tests, to identify potential security issues early.
5. **Documentation**: Document any security-related features or configuration to assist users in maintaining secure deployments.

## Future Enhancements

We are continuously improving Netmikro's security. Users and contributors are encouraged to provide feedback and suggestions for enhancing the security of the project.

## Contact

For security issues or inquiries, please reach out to [security@henriquesebastiao.com](mailto:security@henriquesebastiao.com).