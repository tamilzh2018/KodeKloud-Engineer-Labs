# Contributing to 100 Days of DevOps

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Ways to Contribute

### 1. Report Issues
- Found a bug? Report it!
- Solution doesn't work? Let us know!
- Documentation unclear? Tell us how to improve!

### 2. Improve Solutions
- Have a better approach? Share it!
- Found a more efficient solution? Contribute!
- Know best practices we missed? Help us improve!

### 3. Enhance Documentation
- Fix typos or grammar
- Add clarifications
- Include additional examples
- Improve explanations

### 4. Add Resources
- Share helpful links
- Add diagrams or visuals
- Contribute reference materials
- Create video tutorials

### 5. Share Your Experience
- Help others in Discussions
- Answer questions
- Share your learning journey
- Provide feedback

---

## 🚀 Getting Started

### Fork and Clone

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR-USERNAME/100-days-of-devops.git
cd 100-days-of-devops

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/100-days-of-devops.git
```

### Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a fix branch
git checkout -b fix/issue-description
```

---

## 📝 Contribution Guidelines

### Code Style

**Markdown**
- Use proper heading hierarchy
- Include code blocks with language tags
- Add blank lines between sections
- Use consistent formatting

**Shell Scripts**
- Include shebang (`#!/bin/bash`)
- Add comments for complex logic
- Use meaningful variable names
- Follow shellcheck recommendations

**Python**
- Follow PEP 8 style guide
- Include docstrings
- Add type hints where appropriate
- Keep functions focused and small

**Configuration Files**
- Add inline comments
- Use consistent indentation
- Include examples
- Document parameters

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add alternative solution for Day 15 NGINX SSL setup"
git commit -m "Fix broken link in Week 3 README"
git commit -m "Improve explanation of Docker networking in Day 42"

# Not so good
git commit -m "Update file"
git commit -m "Fix stuff"
git commit -m "WIP"
```

**Format**: `<type>: <description>`

Types:
- `feat`: New feature or solution
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `style`: Formatting, typos
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

---

## 🔄 Pull Request Process

### 1. Sync with Upstream

```bash
# Fetch upstream changes
git fetch upstream

# Merge with main
git merge upstream/main
```

### 2. Make Your Changes

- Make focused, logical changes
- Test your changes thoroughly
- Update documentation if needed
- Add new resources to appropriate directories

### 3. Commit and Push

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add alternative solution for Day 5"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Create Pull Request

- Go to GitHub and create a Pull Request
- Use a clear title and description
- Reference any related issues
- Add screenshots if relevant
- Request review

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
Describe how you tested your changes

## Related Issues
Closes #123

## Screenshots (if applicable)
Add screenshots here
```

---

## ✅ Checklist Before Submitting

- [ ] Code follows project style guidelines
- [ ] Changes have been tested
- [ ] Documentation has been updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] All files are properly formatted
- [ ] No sensitive information included

---

## 🐛 Reporting Issues

### Bug Reports

Use this template:

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 20.04
- Docker version: 20.10.7
- Python version: 3.9.5

**Screenshots**
If applicable

**Additional Context**
Any other relevant information
```

### Feature Requests

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this address?

**Proposed Solution**
How should it work?

**Alternatives Considered**
What other approaches did you consider?

**Additional Context**
Any mockups, examples, or references
```

---

## 💡 Content Guidelines

### Adding Solutions

When contributing solutions:

1. **Explain the Why**: Don't just show commands, explain reasoning
2. **Include Verification**: Show how to verify the solution works
3. **Add Learning Notes**: What concepts does this demonstrate?
4. **Consider Alternatives**: Are there other approaches?
5. **Security First**: Point out security considerations
6. **Best Practices**: Mention industry standards

### Improving Documentation

- Use clear, simple language
- Include examples
- Add diagrams where helpful
- Link to official documentation
- Keep it up to date

### Adding Resources

- Verify links work
- Use official documentation when possible
- Include brief descriptions
- Organize logically
- Keep it relevant

---

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers warmly
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Not Acceptable

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Unprofessional conduct

### Enforcement

Maintainers will:
- Review and address violations
- Remove inappropriate content
- Ban repeat offenders if necessary
- Act fairly and transparently

---

## 📧 Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions
- **Email**: For sensitive matters only

---

## 🎓 Learning Resources

New to contributing? Check these out:

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [Markdown Guide](https://www.markdownguide.org/)

---

## 🏆 Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Special mentions in README
- Hall of fame (for significant contributions)

---

## ❓ Questions?

- Check existing issues and discussions
- Ask in GitHub Discussions
- Review documentation
- Contact maintainers

---

**Thank you for contributing to 100 Days of DevOps! Together we can create an amazing learning resource for the DevOps community! 🚀**

---

[← Back to Main README](./README.md)
