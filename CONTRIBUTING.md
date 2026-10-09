# Contributing to MX-CARD Agent

Welcome! We're excited to have you contribute to MX-CARD Agent. This document outlines the contribution guidelines to help you navigate the process smoothly and ensure a positive experience for all contributors.

## Welcome

First, thank you for your interest in contributing! Whether it's fixing a bug, improving documentation, or adding a new feature, your help makes this project better for everyone.

## How to Contribute

### 1. Getting Started

#### Prerequisites

- Python 3.11+
- Git
- Any code editor (VS Code, IntelliJ, etc.)

#### Fork and Clone

1. **Fork the repository**: Click the "Fork" button in the upper right corner of this repository
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/MX-CARD_Agent.git
   cd MX-CARD_Agent
   ```

3. **Add the original as upstream**:
   ```bash
   git remote add upstream https://github.com/addymistrel/MX-CARD_Agent.git
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 2. Understanding the Project

#### Project Overview

MX-CARD Agent is an AI assistant built with:
- **LangGraph** for workflow orchestration
- **Rich TUI** for terminal interface
- **14+ built-in tools** + MCP integration
- **Advanced safety systems**

#### Key Areas for Contribution

**Code Contributions**:
- Core agent logic (`agent/`)
- Built-in tools (`tools/builtin/`)
- UI components (`ui/`)
- Configuration system (`config/`)

**Documentation**:
- README improvements
- HOW_TO_USE.md updates
- Example workflows
- API documentation

**Testing & Quality**:
- Unit tests for new features
- Code review participation
- Performance improvements
- Bug fixes

#### Development Workflow

1. **Read the codebase**: Explore the structure and understand existing patterns
2. **Check for existing issues**: Look for open issues that match your interests
3. **Ask questions**: Use GitHub Discussions or Issues for unclear requirements
4. **Plan your work**: Break down complex tasks into manageable steps

### 3. Making Changes

#### Code Standards

- **Python version**: Python 3.11+
- **Code style**: Follow existing project patterns
- **Documentation**: Include docstrings for new functions/methods
- **Testing**: Write tests for new functionality
- **Naming**: Use descriptive, consistent naming

#### Workflow

1. **Make small, focused commits**: One change per commit when possible
2. **Use descriptive commit messages**:
   ```
   git commit -m "feat: add new read_file optimization
   
   - Implements chunked reading for large files
   - Adds progress feedback
   - Closes #123
   "
   ```

3. **Test your changes**: Run existing tests to ensure you haven't broken anything
4. **Write tests**: Add tests for new features and edge cases

### 4. Testing

#### Running Tests

While the project currently doesn't have a formal test suite, we recommend:

1. **Manual testing**: Test your changes interactively
2. **Code review**: Have others review your changes
3. **Edge case testing**: Test with various inputs and scenarios

#### Testing Guidelines

- Test both normal and edge cases
- Test with different file types and sizes
- Test error conditions and error messages
- Test with various approval policies

### 5. Pull Requests

#### Before Opening a PR

1. **Ensure tests pass**: Run your changes through a reasonable test suite
2. **Update documentation**: Add or update documentation as needed
3. **Create a clear PR description**: Explain what you're doing and why
4. **Rebase onto main**: Ensure your branch is up to date

#### PR Template

Use this template for your pull request:

```markdown
## Summary
[Brief description of your changes]

## Changes Made
- [ ] List specific changes
- [ ] Documentation updates
- [ ] Bug fixes
- [ ] New features

## Testing
- [ ] Manual testing completed
- [ ] Edge cases covered
- [ ] Existing tests pass

## Impact
- [ ] Improved performance
- [ ] New functionality
- [ ] Bug fix
- [ ] Documentation improvement

## Related Issues
- Fixes #123
- Related to #456

## Notes
[Any additional context or considerations]
```

#### PR Review Process

1. **Automatic checks**: CI will run if configured
2. **Code review**: Reviewers will examine the changes
3. **Feedback loop**: Address any feedback or requests
4. **Merge approval**: Get approval from project maintainers

### 6. Branching Strategy

We use GitFlow principles:

- **Main**: Production-ready code
- **Develop**: Current development work
- **Feature branches**: Work on specific features/issues
- **Release branches**: Prepare for new releases

#### Branch Naming Conventions

```
feature/      - New features
bugfix/      - Bug fixes
docs/        - Documentation changes
refactor/    - Code refactoring
test/        - Test additions/modifications
chore/       - Maintenance tasks
```

### 7. Communication

#### Asking for Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For general questions and planning
- **Code reviews**: For feedback on pull requests

#### Sharing Your Progress

- **Regular updates**: Share progress during long tasks
- **Screenshots**: Share relevant output when debugging
- **Logs**: Include relevant logs when reporting issues

### 8. Community Guidelines

#### Code of Conduct

Please follow these community guidelines:

- **Be respectful**: Treat all contributors with respect
- **Stay focused**: Keep discussions on topic
- **Help others**: Share knowledge and assist when possible
- **Be patient**: Everyone works at their own pace

#### Conflict Resolution

If conflicts arise:

1. **Discuss openly**: Address concerns directly
2. **Seek mediation**: Ask neutral parties for help
3. **Focus on facts**: Base decisions on technical merit
4. **Document decisions**: Record resolutions for future reference

### 9. Security Considerations

#### Safe Practices

- **Input validation**: Always validate user input
- **Output escaping**: Properly escape output to prevent injection
- **Path safety**: Restrict operations to intended directories
- **Environment filtering**: Be careful with environment variables

#### Security Review

For security-sensitive changes:

1. **Review code carefully**: Look for common vulnerabilities
2. **Test security implications**: Test edge cases
3. **Document security considerations**: Note any security tradeoffs

### 10. Attribution and Credit

#### Giving Credit

- **Contributors**: Add your name to CONTRIBUTORS.md if you'd like
- **Bug reports**: Credit those who help find issues
- **Feature requests**: Acknowledge those who suggest improvements
- **Documentation**: Credit contributors who improve docs

#### Acknowledgments

- Thank contributors who provide significant help
- Acknowledge community feedback
- Credit external resources used

### 11. Legal and Compliance

#### License Compliance

- **Existing licenses**: Respect all existing licenses
- **New dependencies**: Check licenses before adding new ones
- **Copyright holders**: Maintain proper attribution

#### Contribution License Agreement

By contributing, you agree:

- Your contribution is original and you have the right to share it
- You grant a non-exclusive license for the project to use your contribution
- Your contribution doesn't violate any existing licenses

## Special Contribution Areas

### Improving the Agent's Intelligence

Help make MX-CARD Agent smarter:

- **Add new tools**: Create domain-specific tools
- **Improve reasoning**: Add better planning or analysis capabilities
- **Enhance memory**: Better context retention and retrieval
- **Optimize performance**: Faster tool execution or better caching

### Expanding Tool Ecosystem

Contribute new tools:

- **Domain tools**: Weather, database, cloud services
- **Integration tools**: Git, CI/CD, monitoring
- **Productivity tools**: File management, note-taking
- **Research tools**: Web search, data analysis

### Documentation and Examples

Help others get started:

- **Tutorials**: Step-by-step guides
- **Examples**: Real-world usage scenarios
- **API docs**: Reference documentation
- **Best practices**: Recommended patterns and workflows

### Accessibility and UX

Improve the user experience:

- **TUI enhancements**: Better terminal interface
- **Accessibility**: Support for different terminals
- **Internationalization**: Multi-language support
- **Documentation**: Clearer explanations and examples

## Getting Started with Your First Contribution

1. **Pick an issue**: Choose something that interests you
2. **Comment on the issue**: Let the maintainers know you're working on it
3. **Start developing**: Fork, clone, and work on your branch
4. **Stay connected**: Keep maintainers updated
5. **Submit your work**: Create a pull request

## Frequently Asked Questions

### I don't know Python well. Can I still contribute?

Absolutely! We welcome contributions at all skill levels. Start with documentation, bug fixes, or small improvements. Ask questions when you're unsure.

### How much time should I commit?

There are no time requirements. Contributions can be as small as fixing a typo or as large as implementing a major feature. The most important thing is that you enjoy what you're doing.

### What if I want to contribute but there's nothing I'm interested in?

Don't hesitate to open an issue with "Good First Issue" or suggest new features. Every contribution helps shape the project.

### How often should I update my branch?

Regular updates help avoid merge conflicts. Update from main at least once a week:

```bash
git checkout develop
git pull origin develop
# Then switch back to your feature branch
git checkout feature/your-feature-name
git rebase develop
```

### What if my pull request gets rejected?

Don't be discouraged! Receiving feedback is a normal part of open-source contribution. Rejections are usually about approach or timing, not the value of your contribution. Use the feedback to improve and try again, or start a new discussion.

## Additional Resources

- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Python Documentation](https://docs.python.org/3/)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Rich Documentation](https://rich.readthedocs.io/)

## Thank You!

Your contributions make MX-CARD Agent better and more accessible to everyone. Whether you've contributed code, documentation, or just your time and ideas, you've helped create something valuable.

We look forward to working with you on this journey!

---

*This CONTRIBUTING.md file was created to help our open-source community thrive. If you have suggestions for improving these guidelines, please let us know!*