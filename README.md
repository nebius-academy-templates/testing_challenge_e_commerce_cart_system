In this task, you'll team up with Cursor to write unit tests for a shopping cart system that cover all the core functionality and edge cases.

## 🛒 Project and goal


The core features of the shopping cart system are implemented in the `ShoppingCart` class:

- Adding items to the cart
- Removing items from the cart
- Calculating totals with tax and discounts
- Applying discount codes
- Validating inventory availability
- Managing cart persistence

Your goal is to:

1. Understand the business logic
2. Generate comprehensive unit tests covering happy paths, edge cases, and error conditions
3. Achieve >90% test coverage with meaningful tests
4. Document your testing strategy and approach

## 📂 **Files provided**

| File | Purpose |
| --- | --- |
| `shopping_cart.py` | Main `ShoppingCart` class |
| `product.py` | Product model (pricing, inventory) |
| `discount_codes.py` | Discount code validation logic |
| `inventory_service.py` | External inventory-checking service |
| `test_requirements.txt` | Testing dependencies (pytest, coverage, etc.) |

## **🔍 Step 1: Analyze the system**

Start by understanding the system's logic and structure. Use Cursor to explore the code with questions like:

- What does each method do?
- What are the possible failure scenarios?
- What edge cases need to be tested?
- What external dependencies exist?

## **📝 Step 2: Create a test plan**

Use Cursor to create a test plan document called `test_plan.md`. It should outline:

- Methods under test
- Test scenarios (happy path, edge cases, errors)
- Mocking strategy and test data setup
- Coverage targets and risk assessment

## **🧪 Step 3: Write the tests**

Generate comprehensive unit tests based on your plan:

- Happy path tests for all core functionality
- Edge case tests (empty cart, invalid items, etc.)
- Error condition tests (network failures, invalid data)
- Boundary tests (minimum/maximum values)

## **📊 Step 4: Measure coverage**

Run a coverage analysis and identify any gaps. If needed, add more tests to fill them.

Document your coverage results in `coverage_report.md`.

## **💡 Advanced challenges (optional)**

1. **Property-based testing**: Use `hypothesis` to generate test cases.
2. **Performance testing**: Add tests for cart performance under load.
3. **Integration tests**: Test the cart with a real database or services.
4. **Mutation testing**: Use `mutmut` to evaluate your test quality.
5. **CI/CD integration**: Set up automated test running.

## 📖 Requirements

Read the testing requirements and recommendations below. Make sure your project meets them.

## **Required test categories**

### **1. Cart management**

```
class TestCartManagement:
    # Test adding items to cart
    # Test removing items from cart
    # Test updating item quantities
    # Test clearing the cart
    # Test cart persistence
```

### **2. Price calculation**

```
class TestPriceCalculations:
    # Test basic total calculation
    # Test tax calculation
    # Test discount application
    # Test multiple discount scenarios
    # Test price precision/rounding
```

### **3. Discount code**

```
class TestDiscountCodes:
    # Test valid discount codes
    # Test expired discount codes
    # Test invalid discount codes
    # Test discount code limits
    # Test discount code combinations
```

### **4. Inventory validation**

```
class TestInventoryValidation:
    # Test sufficient inventory
    # Test insufficient inventory
    # Test inventory service failures
    # Test concurrent inventory updates
    # Test inventory edge cases
```

### **5. Error handling**

```
class TestErrorHandling:
    # Test invalid input data
    # Test network failures
    # Test service unavailability
    # Test malformed responses
    # Test timeout scenarios
```

## **Testing requirements**

### **Test coverage goals**

- **Overall coverage**: >90%
- **Branch coverage**: >85%
- **Critical path coverage**: 100%

### **Test quality standards**

- **Isolated**: Each test should be independent.
- **Fast**: All tests should run quickly (<5 seconds total).
- **Reliable**: Tests should pass consistently.
- **Maintainable**: Tests should be easy to understand and modify.
- **Meaningful**: Tests should catch real bugs.

### **Mocking strategy**

- Mock external services (inventory, payment, email).
- Don't mock the system under test.
- Use dependency injection where needed.
- Keep mocks simple and focused.

## **Test scenarios**

### **Cart operations**

- Add a single item/multiple items to the cart
- Add the same item multiple times
- Remove an item from the cart
- Remove a non-existent item
- Update item quantity to zero
- Update item quantity to a negative number

### **Price calculations**

- Calculate the total for a single item
- Calculate the total for multiple items
- Calculate tax on various amounts
- Apply a percentage discount
- Apply a fixed amount discount
- Apply multiple discounts
- Handle currency precision

### **Edge cases**

- Empty cart operations
- Maximum cart size limits
- Very large quantities
- Zero-priced items
- Negative prices (refunds)
- Currency conversion scenarios

### **Error conditions**

- Invalid product IDs
- Unavailable products
- Inventory service down
- Invalid discount codes
- Network timeouts
- Database connection failures

## **Testing best practices**

- Test behavior, not implementation.
- Use descriptive test names: e.g. `should_apply_percentage_discount_correctly`.
- Follow AAA (Arrange — Act — Assert).
- Aim for one assertion per test.
- Verify error messages for clarity.

## **Documentation requirements**

1. `test_plan.md`: Strategy, scenarios, mocking, targets, risks.

```
#Shopping Cart Test Plan

##Test strategy[Your approach to testing this system]

##Test scenarios[Comprehensive list of what you're testing]

##Mocking strategy[How you'll handle external dependencies]

##Coverage goals[Your specific coverage targets]

##Risk assessment[What could go wrong and how tests will catch it]
```

2. `coverage_report.md`: Metrics (line/branch/function), gaps, recommendations.

```
#Test Coverage Analysis

##Coverage results
- Line coverage: X%
- Branch coverage: X%
- Function coverage: X%

##Coverage gaps[Any areas not covered and why]

##Test quality metrics
- Total tests: X
- Test execution time: X seconds
- Test reliability: X% pass rate

##Recommendations[Improvements for better testing]
```

---

## ✅ **Submission checklist**

- [ ]  All cart methods are tested comprehensively
- [ ]  Happy paths, edge cases, and error conditions are covered
- [ ]  Overall coverage >90% and branch coverage >85% achieved
- [ ]  All tests pass consistently
- [ ]  External dependencies are properly mocked
- [ ]  `test_plan.md` and `coverage_report.md` are completed
- [ ]  Tests are well-documented and maintainable

---

When you're done, submit your files. Happy testing! 🧪

---

When submitting, all tests must be in the tests_for_check directory. ❗❗❗
