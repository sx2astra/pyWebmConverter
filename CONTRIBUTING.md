# Contributing to pyWebmConverter

Thank you for your interest in contributing to pyWebmConverter! Here are some guidelines to help you get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/pyWebmConverter.git
   cd pyWebmConverter
   ```

3. **Create a development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Development Setup

Install the package in editable mode with development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

Run the test suite:
```bash
pytest
pytest --cov=pyWebmConverter  # With coverage report
```

## Code Quality

We use pylint for code quality checks:
```bash
pylint pyWebmConverter/
```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear commit messages
3. Push to your fork and create a **Pull Request**

## Pull Request Process

- Ensure all tests pass: `pytest`
- Ensure code passes linting: `pylint pyWebmConverter/`
- Update documentation if needed
- Add a clear description of your changes in the PR

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters

## Reporting Issues

If you find a bug:
1. Check if it's already reported in **Issues**
2. Provide a clear title and description
3. Include steps to reproduce the issue
4. Mention your Python version and OS

## Questions?

Feel free to open an issue with the `question` label if you have any questions.

Thank you for contributing!
