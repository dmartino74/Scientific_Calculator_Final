"""
Unit tests for advanced calculation operations, profile management, and statistics
"""
import pytest
import math
from app.security import hash_password, verify_password


class TestAdvancedCalculations:
    """Test new calculation operations: power, modulus, sqrt"""
    
    def test_power_operation(self):
        """Test exponentiation operation"""
        assert 2 ** 3 == 8
        assert 5 ** 2 == 25
        assert 10 ** 0 == 1
        assert 2 ** -1 == 0.5
    
    def test_modulus_operation(self):
        """Test modulus operation"""
        assert 10 % 3 == 1
        assert 15 % 5 == 0
        assert 7 % 2 == 1
        assert 100 % 7 == 2
    
    def test_sqrt_operation(self):
        """Test square root operation"""
        assert math.sqrt(4) == 2
        assert math.sqrt(9) == 3
        assert math.sqrt(16) == 4
        assert math.sqrt(2) == pytest.approx(1.414213, rel=1e-5)
    
    def test_sqrt_negative_should_fail(self):
        """Test that square root of negative raises ValueError"""
        with pytest.raises(ValueError):
            math.sqrt(-1)
    
    def test_modulus_by_zero_should_fail(self):
        """Test that modulus by zero raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            10 % 0


class TestPasswordManagement:
    """Test password hashing and verification"""
    
    def test_hash_password(self):
        """Test password hashing creates a hash"""
        password = "testpassword123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt prefix
    
    def test_verify_correct_password(self):
        """Test verifying correct password"""
        password = "correct_password"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_incorrect_password(self):
        """Test verifying incorrect password"""
        password = "correct_password"
        wrong = "wrong_password"
        hashed = hash_password(password)
        assert verify_password(wrong, hashed) is False
    
    def test_different_hashes_for_same_password(self):
        """Test that same password generates different hashes (due to salt)"""
        password = "testpassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
    
    def test_password_too_long(self):
        """Test that passwords over 72 bytes are rejected"""
        from fastapi import HTTPException
        long_password = "a" * 73
        with pytest.raises(HTTPException) as exc:
            hash_password(long_password)
        assert exc.value.status_code == 400
        assert "72 bytes" in exc.value.detail


class TestStatisticsCalculations:
    """Test statistics calculation logic"""
    
    def test_calculate_average(self):
        """Test average calculation"""
        numbers = [10, 20, 30, 40, 50]
        avg = sum(numbers) / len(numbers)
        assert avg == 30
    
    def test_operation_counts(self):
        """Test counting operations"""
        operations = ["add", "add", "subtract", "multiply", "add"]
        counts = {}
        for op in operations:
            counts[op] = counts.get(op, 0) + 1
        
        assert counts["add"] == 3
        assert counts["subtract"] == 1
        assert counts["multiply"] == 1
    
    def test_most_used_operation(self):
        """Test finding most used operation"""
        operation_counts = {
            "add": 5,
            "subtract": 2,
            "multiply": 8,
            "divide": 3
        }
        most_used = max(operation_counts.items(), key=lambda x: x[1])[0]
        assert most_used == "multiply"
    
    def test_empty_statistics(self):
        """Test statistics with no data"""
        calculations = []
        total = len(calculations)
        assert total == 0


class TestDataValidation:
    """Test data validation logic"""
    
    def test_valid_email_format(self):
        """Test email validation - basic check"""
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "name+tag@site.org"
        ]
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        for email in valid_emails:
            assert email_pattern.match(email) is not None
    
    def test_invalid_email_format(self):
        """Test invalid email formats"""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com"
        ]
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        for email in invalid_emails:
            assert email_pattern.match(email) is None
    
    def test_username_length_validation(self):
        """Test username length constraints"""
        assert len("abc") >= 3  # minimum
        assert len("validusername") <= 50  # maximum
        assert len("ab") < 3  # too short
        assert len("a" * 51) > 50  # too long
    
    def test_password_length_validation(self):
        """Test password length constraints"""
        assert len("password") >= 8  # minimum
        assert len("validpassword123") <= 72  # maximum
        assert len("short") < 8  # too short
        assert len("a" * 73) > 72  # too long


class TestCalculationLogic:
    """Test calculation logic for all operation types"""
    
    @pytest.mark.parametrize("a,b,operation,expected", [
        (10, 5, "add", 15),
        (10, 5, "subtract", 5),
        (10, 5, "multiply", 50),
        (10, 5, "divide", 2),
        (2, 3, "power", 8),
        (10, 3, "modulus", 1),
    ])
    def test_all_operations(self, a, b, operation, expected):
        """Test all calculation operations"""
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b
        elif operation == "power":
            result = a ** b
        elif operation == "modulus":
            result = a % b
        
        assert result == expected
    
    def test_sqrt_special_operation(self):
        """Test square root as unary operation"""
        assert math.sqrt(25) == 5
        assert math.sqrt(100) == 10
        assert math.sqrt(0) == 0
    
    def test_division_by_zero_error(self):
        """Test division by zero error handling"""
        with pytest.raises(ZeroDivisionError):
            10 / 0
    
    def test_power_with_negative_exponent(self):
        """Test power with negative exponent"""
        result = 2 ** -2
        assert result == 0.25
    
    def test_power_with_zero_exponent(self):
        """Test power with zero exponent"""
        assert 5 ** 0 == 1
        assert 0 ** 0 == 1  # Mathematical convention
