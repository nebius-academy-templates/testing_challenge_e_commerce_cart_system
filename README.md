# Lesson 10: Testing Challenge - E-commerce Cart System

##  Challenge Overview
You have an e-commerce shopping cart system that needs comprehensive unit tests. You'll use Cursor to generate tests that cover the testing pyramid's foundation: **unit tests** (which should be 70% of your testing efforts).

##  The System
The `ShoppingCart` class handles core e-commerce functionality:
- Adding items to the cart
- Removing items from the cart
- Calculating totals with tax and discounts
- Applying discount codes
- Validating inventory availability
- Managing cart persistence

##  Your Mission
Use Cursor to:
1. **Analyse the cart system** and understand all the business logic
2. **Generate comprehensive unit tests** covering happy paths, edge cases, and error conditions
3. **Achieve >90% test coverage** with meaningful tests
4. **Document your testing strategy** and approach

##  Files Provided
- `shopping_cart.py` - The main cart system class
- `product.py` - Product model with pricing and inventory
- `discount_codes.py` - Discount code validation system
- `inventory_service.py` - Inventory checking service
- `test_requirements.txt` - Testing dependencies

##  Success Criteria

### Phase 1: System Analysis 
1. **Use Cursor to analyse the cart system**
   - What are all the methods and their responsibilities?
   - What are the possible failure scenarios?
   - What edge cases need to be tested?
   - What external dependencies exist?

### Phase 2: Test Planning 
2. **Create a test plan document**
   - List all methods that need testing
   - Identify test scenarios for each method
   - Plan your mocking strategy for external dependencies
   - Define your test data setup

### Phase 3: Test Implementation 
3. **Generate comprehensive unit tests**
   - Happy path tests for all core functionality
   - Edge case tests (empty cart, invalid items, etc.)
   - Error condition tests (network failures, invalid data)
   - Boundary tests (minimum/maximum values)

### Phase 4: Coverage Analysis
4. **Measure and analyse test coverage**
   - Run coverage analysis
   - Identify any gaps in coverage
   - Add additional tests if needed
   - Document coverage results

##  Required Test Categories

### 1. Cart Management Tests
```python
class TestCartManagement:
    # Test adding items to cart
    # Test removing items from cart  
    # Test updating item quantities
    # Test clearing the cart
    # Test cart persistence
```

### 2. Price Calculation Tests
```python
class TestPriceCalculations:
    # Test basic total calculation
    # Test tax calculation
    # Test discount application
    # Test multiple discount scenarios
    # Test price precision/rounding
```

### 3. Discount Code Tests
```python
class TestDiscountCodes:
    # Test valid discount codes
    # Test expired discount codes
    # Test invalid discount codes
    # Test discount code limits
    # Test discount code combinations
```

### 4. Inventory Validation Tests
```python
class TestInventoryValidation:
    # Test sufficient inventory
    # Test insufficient inventory
    # Test inventory service failures
    # Test concurrent inventory updates
    # Test inventory edge cases
```

### 5. Error Handling Tests
```python
class TestErrorHandling:
    # Test invalid input data
    # Test network failures
    # Test service unavailability
    # Test malformed responses
    # Test timeout scenarios
```

##  Testing Requirements

### Test Coverage Goals:
- **Overall Coverage**: >90%
- **Branch Coverage**: >85%
- **Critical Path Coverage**: 100%

### Test Quality Standards:
- **Isolated**: Each test should be independent
- **Fast**: All tests should run quickly (<5 seconds total)
- **Reliable**: Tests should pass consistently
- **Maintainable**: Tests should be easy to understand and modify
- **Meaningful**: Tests should catch real bugs

### Mocking Strategy:
- Mock external services (inventory, payment, email)
- Don't mock the system under test
- Use dependency injection where needed
- Keep mocks simple and focused

##  Specific Test Scenarios

### Cart Operations:
- Add single item to empty cart
- Add multiple items to cart
- Add same item multiple times
- Remove item from cart
- Remove non-existent item
- Update item quantity to zero
- Update item quantity to negative number

### Price Calculations:
- Calculate total for single item
- Calculate total for multiple items
- Calculate tax on various amounts
- Apply percentage discount
- Apply fixed amount discount
- Apply multiple discounts
- Handle currency precision

### Edge Cases:
- Empty cart operations
- Maximum cart size limits
- Very large quantities
- Zero-priced items
- Negative prices (refunds)
- Currency conversion scenarios

### Error Conditions:
- Invalid product IDs
- Unavailable products
- Inventory service down
- Invalid discount codes
- Network timeouts
- Database connection failures

##  Documentation Requirements

### 1. Test Plan Document
```markdown
# Shopping Cart Test Plan

## Test Strategy
[Your approach to testing this system]

## Test Scenarios
[Comprehensive list of what you're testing]

## Mocking Strategy  
[How you'll handle external dependencies]

## Coverage Goals
[Your specific coverage targets]

## Risk Assessment
[What could go wrong and how tests will catch it]
```

### 2. Test Coverage Report
```markdown
# Test Coverage Analysis

## Coverage Results
- Line Coverage: X%
- Branch Coverage: X%
- Function Coverage: X%

## Coverage Gaps
[Any areas not covered and why]

## Test Quality Metrics
- Total Tests: X
- Test Execution Time: X seconds
- Test Reliability: X% pass rate

## Recommendations
[Improvements for better testing]
```

##  Advanced Challenge (Optional)
1. **Property-based testing**: Use hypothesis to generate test cases
2. **Performance testing**: Add tests for cart performance under load
3. **Integration tests**: Test cart with real database/services
4. **Mutation testing**: Use mutmut to test your test quality
5. **CI/CD integration**: Set up automated test running

##  Testing Best Practices
- **Test behaviour, not implementation**: Focus on what the code does, not how
- **Use descriptive test names**: Tests should read like documentation
- **Follow AAA pattern**: Arrange, Act, Assert
- **One assertion per test**: Keep tests focused and simple
- **Test error messages**: Ensure errors provide useful information

##  Common Testing Pitfalls
- **Testing too much**: Don't test framework code or external libraries
- **Brittle tests**: Tests that break when implementation changes
- **Slow tests**: Tests that take too long discourage running them
- **Unclear tests**: Tests that don't explain what they're verifying
- **Missing edge cases**: Not testing boundary conditions and error scenarios

##  Submission Checklist
- [ ] All cart methods have comprehensive tests
- [ ] Happy path, edge cases, and error conditions covered
- [ ] Test coverage >90% achieved
- [ ] All tests pass consistently
- [ ] External dependencies properly mocked
- [ ] Test plan and coverage report completed
- [ ] Tests are well-documented and maintainable

---

**This challenge teaches you to use Cursor for generating comprehensive unit tests that form the foundation of a solid testing strategy.** 
