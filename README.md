# Manchester Stock Exchange (MSEG)

## Introduction

The Manchester Stock Exchange (MSEG) system has been implemented as a comprehensive stock market management platform designed to meet key requirements for managing company applications, stock listings, and trading operations. The implementation follows a modular architecture with clear separation of concerns across authentication, database management, UI components, and business logic layers.

The project was conducted through a systematic approach that prioritizes scalability, maintainability, and user experience. Core functionality includes a dual-portal system serving both stock exchange managers and registered companies, with role-based access control ensuring appropriate permissions. The manager portal enables review and approval of company listing applications, while the company portal allows businesses to submit applications and monitor their stock performance. The stock market module provides real-time visualizations of stock prices with historical data tracking over 366 days, implementing a realistic random walk pricing model.

The implementation methodology focused on meeting key requirements including secure user authentication, efficient database operations with referential integrity, responsive graphical interfaces with theme support, and comprehensive test coverage as documented in the TEST_PLAN.md file.

## 5. System Requirements

### 5.1 Software Requirements

The MSEG system is built using **Python** as the primary programming language and **SQLite3** as the database engine. Python was selected for its rapid development capabilities, extensive standard library support, and excellent compatibility with the Tkinter GUI framework. The language's simplicity and readability facilitate efficient implementation of complex business logic while maintaining code maintainability.

SQLite3 was chosen as the database solution due to its zero-configuration setup, serverless architecture, and seamless integration with Python's standard library. This combination ensures MSEG can be deployed quickly without external database server dependencies, making it ideal for both development and production environments. The embedded database approach eliminates network latency and simplifies the deployment process.

Both Python and SQLite3 are compatible with all major IDEs including PyCharm, Visual Studio Code, Sublime Text, and IDLE, providing developers flexibility in their development environment. The lightweight nature of these technologies ensures the MSEG system remains portable and easy to configure across different platforms.

### 5.2 Hardware Requirements

**Operating System Compatibility:**
- Windows 10 or later
- macOS 10.14 or later
- Linux (Ubuntu 18.04+, Fedora 30+, or equivalent distributions)

**Minimum Specifications:** 2GB RAM, 100MB disk space, 1280x720 display resolution
