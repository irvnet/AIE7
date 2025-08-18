# Workflow Patterns - IBM Tiger AI Detective

## 🔄 Development Flow

### Standard Development Cycle:
1. **Check Current Status**
   ```bash
   git status
   git log --oneline -3
   # Review PROJECT_CONTEXT.md for current state
   ```

2. **Make Incremental Changes**
   - Small, focused changes
   - Test each change
   - Document significant decisions

3. **Test Changes**
   ```bash
   uv run python test_system.py    # System health check
   uv run python -m pytest tests/  # Unit tests
   uv run streamlit run app/main.py  # Manual testing
   ```

4. **Commit with Descriptive Messages**
   ```bash
   git add .
   git commit -m "feat: Add [specific feature] with [rationale]"
   ```

5. **Update Context Files**
   - Update `PROJECT_CONTEXT.md` for significant changes
   - Update `.ai-context/` files if patterns change

### Feature Development Pattern:
```
1. Plan → 2. Implement → 3. Test → 4. Commit → 5. Document
```

## 🐛 Error Handling Workflow

### When Errors Occur:
1. **Document the Error**
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior

2. **Check Common Issues**
   - Review `.ai-context/troubleshooting.md`
   - Check recent commits for changes
   - Verify environment setup

3. **Debug Methodically**
   ```bash
   # Check system health
   uv run python test_system.py
   
   # Check database
   uv run python -c "from app.models.database import engine; print('DB OK')"
   
   # Check dependencies
   uv sync
   ```

4. **Fix and Test**
   - Make minimal changes
   - Test the fix
   - Document the solution

5. **Update Troubleshooting Guide**
   - Add to `.ai-context/troubleshooting.md`
   - Update relevant context files

### Common Error Patterns:
- **SQLAlchemy DetachedInstanceError** → Check session management
- **PDF Download Failures** → Check network and URLs
- **Mock Data Issues** → Clear database and regenerate
- **Import Errors** → Check `uv sync` and dependencies

## 🤝 Collaboration Patterns

### Working with AI Assistant:
1. **Provide Context**
   - Reference `PROJECT_CONTEXT.md`
   - Mention current commit or status
   - Specify what you're trying to achieve

2. **Review Suggestions**
   - Check code against standards
   - Test before committing
   - Ask for clarification if needed

3. **Iterate Together**
   - Make small changes
   - Test each iteration
   - Document decisions

### Code Review Process:
1. **Self-Review**
   - Check against coding standards
   - Run tests
   - Verify functionality

2. **AI Review**
   - Ask for code review
   - Request improvements
   - Check for best practices

3. **Documentation Update**
   - Update relevant context files
   - Add comments for complex logic
   - Update commit messages

## 📋 Task Management

### Task Prioritization:
1. **Critical Path** - Blocking other work
2. **High Value** - Core functionality
3. **Nice to Have** - Enhancements
4. **Technical Debt** - Code quality

### Task Breakdown:
- **Small tasks** (1-2 hours) - Implement directly
- **Medium tasks** (4-8 hours) - Break into smaller pieces
- **Large tasks** (1+ days) - Create detailed plan

### Progress Tracking:
- **Git commits** as progress markers
- **PROJECT_CONTEXT.md** for status updates
- **Checklist format** for task completion

## 🔧 Environment Management

### Development Setup:
```bash
# Initial setup
uv sync
uv run python setup.py

# Daily workflow
git pull
uv run streamlit run app/main.py
```

### Environment Variables:
```bash
# Required
export OPENAI_API_KEY="your_key_here"

# Optional
export TAVILY_API_KEY="your_key_here"
export DATABASE_URL="sqlite:///./tiger_team_support.db"
```

### Dependency Management:
- **Use `uv`** for all package management
- **Update `pyproject.toml`** for new dependencies
- **Run `uv sync`** after dependency changes
- **Test** after dependency updates

## 📝 Documentation Workflow

### When to Update Documentation:
- **New features** added
- **Architecture changes** made
- **Bug fixes** that affect workflow
- **Environment changes** (new dependencies, etc.)

### Documentation Standards:
- **Clear and concise** language
- **Step-by-step** instructions
- **Examples** for complex procedures
- **Troubleshooting** sections

### File Update Priority:
1. **PROJECT_CONTEXT.md** - Project state
2. **.ai-context/README.md** - AI instructions
3. **.ai-context/troubleshooting.md** - Error solutions
4. **README.md** - User documentation

## 🚀 Deployment Workflow

### Pre-Deployment Checklist:
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Performance tested

### Deployment Steps:
1. **Local Testing**
   ```bash
   uv run streamlit run app/main.py
   # Test all features manually
   ```

2. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: Ready for deployment"
   git push
   ```

3. **Deploy to Vercel**
   - Automatic deployment from git push
   - Monitor deployment logs
   - Test deployed application

4. **Post-Deployment**
   - Verify all features work
   - Check error logs
   - Update documentation if needed

## 🔄 Iteration Patterns

### Rapid Prototyping:
1. **Quick Implementation** - Get it working
2. **Test and Refine** - Improve functionality
3. **Document and Commit** - Save progress
4. **Repeat** - Iterate on feedback

### Quality Assurance:
1. **Code Review** - Check against standards
2. **Testing** - Unit and integration tests
3. **Documentation** - Update relevant files
4. **Deployment** - Deploy and verify

### Continuous Improvement:
- **Regular reviews** of workflow efficiency
- **Update patterns** based on experience
- **Share learnings** in context files
- **Refine processes** over time

---

**Last Updated**: August 18, 2024
